# -*- coding: utf-8 -*-
#
# MIT License
# 
# Copyright (c) 2021 Tianyuan Langzi
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


"""
WxGL: 基于pyopengl的三维数据可视化库

WxGL以wx为显示后端，提供matplotlib风格的交互绘图模式
同时，也可以和wxpython无缝结合，在wx的窗体上绘制三维模型
"""


import wx
from wx import glcanvas
import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *

from . import region
from . import cm
from . import fm


class WxGLScene(glcanvas.GLCanvas):
    """GL场景类"""
    
    def __init__(self, parent, **kwds):
        """构造函数
        
        parent      - 父级窗口对象
        kwds        - 关键字参数
                        proj        - 投影模式，字符串
                            'ortho'     - 平行投影
                            'cone'      - 透视投影
                        mode        - 2D/3D模式，字符串
                            '2D'        - 2D模式，y轴向上
                            '3D'        - 3D模式，z轴向上
                        oecs        - 视点坐标系（Eye Coordinate System）原点
                        dist        - 眼睛与ECS原点的距离
                        azimuth     - 方位角
                        elevation   - 仰角
                        view        - 视景体
                        zoom        - 视口缩放因子
                        interval    - 定时器间隔（毫秒）
                        style       - 场景风格
                            'white'     - 珍珠白
                            'black'     - 石墨黑
                            'gray'      - 国际灰
                            'blue'      - 太空蓝
                            'royal'     - 宝石蓝
        """
        
        for key in kwds:
            if key not in ['proj', 'mode', 'oecs', 'dist', 'azimuth', 'elevation', 'view', 'zoom', 'interval', 'style']:
                raise KeyError('不支持的关键字参数：%s'%key)
        
        self.parent = parent                                                # 父级窗口对象
        while not isinstance(self.parent, wx.Frame):
            self.parent = self.parent.parent
        
        self.proj = kwds.get('proj', 'cone')                                # 投影模式，默认透视投影
        self.mode = kwds.get('mode', '3D').upper()                          # 设置2D/3D模式，默认3D模式
        self.oecs = np.array(kwds.get('oecs', [0.0,0.0,0.0]))               # ECS原点，默认与OCS（目标坐标系）原点重合
        self.dist = kwds.get('dist', 5)                                     # 眼睛与ECS原点的距离，默认5个单位
        self.azimuth = kwds.get('azimuth', 0)                               # 方位角，默认0°
        self.elevation = kwds.get('elevation', 0)                           # 仰角，默认0°
        self.view = np.array(kwds.get('view', [-1,1,-1,1,2.6,1000]))        # 视景体
        self.zoom = kwds.get('zoom', 1.0 if self.proj=='cone' else 1.5)     # 视口缩放因子，默认1
        self.interval = kwds.get('interval', 25)                            # 定时器间隔，默认25毫秒
        self.style = self._set_style(kwds.get('style', 'blue'))             # 设置风格（背景和文本颜色）
        
        self.eye = None                                                     # 眼睛的位置
        self.up = None                                                      # 向上的方向
        self.store = dict()                                                 # 存储相机姿态、缩放比例等
        self.rotate = None                                                  # 相机自动水平旋转角度
        self._set_eye_and_up(save=True)                                     # 根据方位角、仰角和距离设置眼睛位置和向上的方向
        
        self.fm = fm.FontManager()                                          # 字体管理对象
        self.cm = cm.ColorManager()                                         # 颜色管理对象
        self.grid_is_show = True                                            # 是否显示网格
        
        glcanvas.GLCanvas.__init__(self, parent, -1, style=glcanvas.WX_GL_RGBA|glcanvas.WX_GL_DOUBLEBUFFER|glcanvas.WX_GL_DEPTH_SIZE)
        
        self.size = self.GetClientSize()                                    # OpenGL窗口的大小
        self.context = glcanvas.GLContext(self)                             # OpenGL上下文
        self.regions = list()                                               # 存储视区信息
        self.subgraphs = list()                                             # 存储子图信息
        self.mpos = wx._core.Point()                                        # 鼠标位置
        
        self.osize = None                                                   # Scene窗口的初始分辨率
        self.tscale = (1,1)                                                 # 和初始分辨率相比，Scene窗口的宽高变化率
        
        self.sys_timer = wx.Timer()                                         # 模型几何变换定时器
        self.sys_n = 0                                                      # 模型几何变换计数器
        
        self._init_gl()                                                     # 画布初始化
        
        self.parent.Bind(wx.EVT_CLOSE, self.on_close)
        self.sys_timer.Bind(wx.EVT_TIMER, self.on_sys_timer)
        
        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_RIGHT_UP, self.on_right_up)
        self.Bind(wx.EVT_MOTION, self.on_mouse_motion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
    
    def _set_style(self, style):
        """设置风格"""
        
        if not style in ('black', 'white', 'gray', 'blue', 'royal'):
            raise ValueError('不支持的风格选项：%s'%style)
        
        if style == 'black':
            return (0.0, 0.0, 0.0, 1.0), (0.9, 0.9, 0.9)
        if style == 'white':
            return (1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 0.0)
        if style == 'gray':
            return (0.9, 0.9, 0.9, 1.0), (0.0, 0.0, 0.3)
        if style == 'blue':
            return (0.0, 0.0, 0.2, 1.0), (0.9, 1.0, 1.0)
        if style == 'royal':
            return (0.133, 0.302, 0.361, 1.0), (1.0, 1.0, 0.9)
    
    def _set_eye_and_up(self, save=False):
        """设置眼睛的位置和向上的方向
        
        save        - 是否保存当前设置，默认不保存
        """
        
        if self.mode == '2D':
            self.eye = np.array([0, 0, self.dist], dtype=np.float)
            self.up = np.array([0,1,0], dtype=np.float)
        else:
            d = self.dist * np.cos(np.radians(self.elevation))
            x = d * np.sin(np.radians(self.azimuth))
            y = -d * np.cos(np.radians(self.azimuth))
            z = self.dist * np.sin(np.radians(self.elevation))
            self.eye = np.array([x, y, z], dtype=np.float)
            
            if -90 < self.elevation < 90:
                self.up = np.array([0,0,1], dtype=np.float)
            else:
                self.up = np.array([0,0,-1], dtype=np.float)
        
        if save:
            self.store.update({
                'oecs': (*self.oecs,),
                'zoom': self.zoom,
                'dist': self.dist,
                'azimuth': self.azimuth,
                'elevation': self.elevation
            })
    
    def on_close(self, evt):
        """点击窗口关闭按钮时"""
        
        self.sys_timer.Stop()
        evt.Skip()
    
    def on_destroy(self, evt):
        """加载场景的应用程序关闭时回收GPU的缓存"""
        
        self.sys_timer.Stop()
        
        for reg in self.regions:
            for id in reg.buffers:
                reg.buffers[id].delete()
        
        evt.Skip()
        
    def on_resize(self, evt):
        """响应窗口尺寸改变事件"""
        
        if self.context:
            self.SetCurrent(self.context)
            self.size = self.GetClientSize()
            self.Refresh(False)
        
        if self.osize is None:
            self.osize = self.GetSize()
        
        evt.Skip()
        
    def on_erase(self, evt):
        """响应背景擦除事件"""
        
        pass
        
    def on_paint(self, evt):
        """响应重绘事件"""
        
        self.repaint()
        evt.Skip()
        
    def on_left_down(self, evt):
        """响应鼠标左键按下事件"""
        
        self.CaptureMouse()
        self.mpos = evt.GetPosition()
        
    def on_left_up(self, evt):
        """响应鼠标左键弹起事件"""
        
        try:
            self.ReleaseMouse()
        except:
            pass
        
    def on_right_up(self, evt):
        """响应鼠标右键弹起事件"""
        
        pass
        evt.Skip()
        
    def on_mouse_motion(self, evt):
        """响应鼠标移动事件"""
        
        if evt.Dragging() and evt.LeftIsDown():
            pos = evt.GetPosition()
            dx, dy = pos - self.mpos
            self.mpos = pos
            
            if self.mode == '3D':
                self.azimuth = (self.azimuth - self.up[2]*0.1*dx)%360
                self.elevation = (self.elevation + 0.1*dy +180)%360 -180
                self._set_eye_and_up()
                self.update_grid()
            else:
                dx = self.zoom*(self.view[1]-self.view[0])*dx/self.size[0]
                dy = self.zoom*(self.view[3]-self.view[2])*dy/self.size[1]
                
                self.oecs[0] -= dx
                self.oecs[1] += dy
                self.eye[0] -= dx
                self.eye[1] += dy
            
            self.Refresh(False)
        
    def on_mouse_wheel(self, evt):
        """响应鼠标滚轮事件"""
        
        if evt.WheelRotation < 0:
            self.zoom *= 1.1
            if self.zoom > 100:
                self.zoom = 100
        elif evt.WheelRotation > 0:
            self.zoom *= 0.9
            if self.zoom < 0.01:
                self.zoom = 0.01
        
        self.Refresh(False)
    
    def on_sys_timer(self, evt):
        """模型定时器函数"""
        
        self.sys_n += 1
        if not self.rotate is None:
            azimuth = self.azimuth + self.rotate
            self.set_posture(azimuth=azimuth)
        
        self.update_grid()
        self.Refresh(False)
    
    def update_grid(self):
        """刷新坐标轴网格"""
        
        if self.mode == '2D' or not self.grid_is_show:
            return
        
        for ax in self.subgraphs:
            reg = ax.reg_main
            if not ax.grid_is_show or not reg.grid:
                continue
            
            if self.elevation > 0:
                reg.hide_model(reg.grid['top'])
                reg.show_model(reg.grid['bottom'])
                reg.hide_model(reg.grid['x_ymin_zmax'])
                reg.hide_model(reg.grid['x_ymax_zmax'])
                reg.hide_model(reg.grid['y_xmin_zmax'])
                reg.hide_model(reg.grid['y_xmax_zmax'])
                
                if 0 <= self.azimuth < 90:
                    reg.show_model(reg.grid['x_ymin_zmin'])
                    reg.hide_model(reg.grid['x_ymax_zmin'])
                    reg.show_model(reg.grid['y_xmax_zmin'])
                    reg.hide_model(reg.grid['y_xmin_zmin'])
                elif 90 <= self.azimuth < 180:
                    reg.hide_model(reg.grid['x_ymin_zmin'])
                    reg.show_model(reg.grid['x_ymax_zmin'])
                    reg.show_model(reg.grid['y_xmax_zmin'])
                    reg.hide_model(reg.grid['y_xmin_zmin'])
                elif 180 <= self.azimuth < 270:
                    reg.hide_model(reg.grid['x_ymin_zmin'])
                    reg.show_model(reg.grid['x_ymax_zmin'])
                    reg.hide_model(reg.grid['y_xmax_zmin'])
                    reg.show_model(reg.grid['y_xmin_zmin'])
                else:
                    reg.show_model(reg.grid['x_ymin_zmin'])
                    reg.hide_model(reg.grid['x_ymax_zmin'])
                    reg.hide_model(reg.grid['y_xmax_zmin'])
                    reg.show_model(reg.grid['y_xmin_zmin'])
            else:
                reg.show_model(reg.grid['top'])
                reg.hide_model(reg.grid['bottom'])
                reg.hide_model(reg.grid['x_ymin_zmin'])
                reg.hide_model(reg.grid['x_ymax_zmin'])
                reg.hide_model(reg.grid['y_xmin_zmin'])
                reg.hide_model(reg.grid['y_xmax_zmin'])
                
                if 0 <= self.azimuth < 90:
                    reg.show_model(reg.grid['x_ymin_zmax'])
                    reg.hide_model(reg.grid['x_ymax_zmax'])
                    reg.show_model(reg.grid['y_xmax_zmax'])
                    reg.hide_model(reg.grid['y_xmin_zmax'])
                elif 90 <= self.azimuth < 180:
                    reg.hide_model(reg.grid['x_ymin_zmax'])
                    reg.show_model(reg.grid['x_ymax_zmax'])
                    reg.show_model(reg.grid['y_xmax_zmax'])
                    reg.hide_model(reg.grid['y_xmin_zmax'])
                elif 180 <= self.azimuth < 270:
                    reg.hide_model(reg.grid['x_ymin_zmax'])
                    reg.show_model(reg.grid['x_ymax_zmax'])
                    reg.hide_model(reg.grid['y_xmax_zmax'])
                    reg.show_model(reg.grid['y_xmin_zmax'])
                else:
                    reg.show_model(reg.grid['x_ymin_zmax'])
                    reg.hide_model(reg.grid['x_ymax_zmax'])
                    reg.hide_model(reg.grid['y_xmax_zmax'])
                    reg.show_model(reg.grid['y_xmin_zmax'])
            
            if 90 <= self.azimuth < 270:
                reg.show_model(reg.grid['front'])
                reg.hide_model(reg.grid['back'])
            else:
                reg.show_model(reg.grid['back'])
                reg.hide_model(reg.grid['front'])
            
            if 0 <= self.azimuth < 180:
                reg.show_model(reg.grid['left'])
                reg.hide_model(reg.grid['right'])
            else:
                reg.show_model(reg.grid['right'])
                reg.hide_model(reg.grid['left'])
            
            if 0 <= self.azimuth < 90:
                reg.show_model(reg.grid['z_xmax_ymax'])
                reg.hide_model(reg.grid['z_xmin_ymax']) 
                reg.hide_model(reg.grid['z_xmin_ymin']) 
                reg.hide_model(reg.grid['z_xmax_ymin']) 
            elif 90 <= self.azimuth < 180:
                reg.hide_model(reg.grid['z_xmax_ymax'])
                reg.show_model(reg.grid['z_xmin_ymax']) 
                reg.hide_model(reg.grid['z_xmin_ymin']) 
                reg.hide_model(reg.grid['z_xmax_ymin']) 
            elif 180 <= self.azimuth < 270:
                reg.hide_model(reg.grid['z_xmax_ymax'])
                reg.hide_model(reg.grid['z_xmin_ymax']) 
                reg.show_model(reg.grid['z_xmin_ymin']) 
                reg.hide_model(reg.grid['z_xmax_ymin']) 
            else:
                reg.hide_model(reg.grid['z_xmax_ymax'])
                reg.hide_model(reg.grid['z_xmin_ymax']) 
                reg.hide_model(reg.grid['z_xmin_ymin']) 
                reg.show_model(reg.grid['z_xmax_ymin']) 
    
    def _wxglDrawElements(self, reg, vars):
        """绘制图元"""
        
        vid, eid, v_type, gl_type, texture = vars
        
        if not texture is None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, texture)
        
        reg.buffers[vid].bind()
        glInterleavedArrays(v_type, 0, None)
        reg.buffers[eid].bind()
        glDrawElements(gl_type, int(reg.buffers[eid].size/4), GL_UNSIGNED_INT, None) 
        reg.buffers[vid].unbind()
        reg.buffers[eid].unbind()
        
        if not texture is None:
            glDisable(GL_TEXTURE_2D)
    
    def _wxglDrawPixels(self, reg, vars):
        """绘制像素"""
        
        k = 1/pow(self.zoom, 1/2)
        pid, rows, cols, pos = vars
        glPixelZoom(k, k)
        glDepthMask(GL_FALSE)
        glRasterPos3fv(pos)
        reg.buffers[pid].bind()
        glDrawPixels(cols, rows, GL_RGBA, GL_UNSIGNED_BYTE, None)
        reg.buffers[pid].unbind()
        glDepthMask(GL_TRUE)
    
    def _init_gl(self):
        """初始化GL"""
        
        self.SetCurrent(self.context)
        
        glClearColor(*self.style[0],)                                       # 设置画布背景色
        glEnable(GL_DEPTH_TEST)                                             # 开启深度测试，实现遮挡关系        
        glDepthFunc(GL_LEQUAL)                                              # 设置深度测试函数
        glShadeModel(GL_SMOOTH)                                             # GL_SMOOTH(光滑着色)/GL_FLAT(恒定着色)
        glEnable(GL_BLEND)                                                  # 开启混合        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)                   # 设置混合函数
        glEnable(GL_ALPHA_TEST)                                             # 启用Alpha测试 
        glAlphaFunc(GL_GREATER, 0.05)                                       # 设置Alpha测试条件为大于0.05则通过
        glEnable(GL_LINE_SMOOTH)                                            # 开启直线反走样
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)                              # 最高质量直线反走样
        glEnable(GL_POLYGON_SMOOTH)                                         # 开启多边形反走样
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)                           # 最高质量多边形反走样
        glEnable(GL_POINT_SMOOTH)                                           # 开启点反走样
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)                             # 最高质量点反走样
        
        glLightfv(GL_LIGHT0, GL_POSITION, (2.0,-20.0,5.0,1.0))              # 光源位置（front）
        glLightfv(GL_LIGHT1, GL_POSITION, (-2.0,20.0,-5.0,1.0))             # 光源位置（rear）
        glLightfv(GL_LIGHT2, GL_POSITION, (-20.0,-2.0,0.0,1.0))             # 光源位置（left）
        glLightfv(GL_LIGHT3, GL_POSITION, (20.0,2.0,0.0,1.0))               # 光源位置（right）
        
        
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)                     # 启用双面渲染
        
    def _draw_gl(self):
        """绘制模型"""
        
        for reg in self.regions:
            x0, y0 = int(reg.box[0]*self.size[0]), int(reg.box[1]*self.size[1])
            w_reg, h_reg = int(reg.box[2]*self.size[0])+1, int(reg.box[3]*self.size[1])
            k = w_reg/h_reg
            
            glViewport(x0, y0, w_reg, h_reg)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            
            if reg.fixed:
                zoom, lookat = reg.zoom, (0,0,5,0,0,0,0,1,0)
            else:
                zoom, lookat = self.zoom, (*self.eye, *self.oecs, *self.up)
            
            if k > 1:
                box = (-zoom*k, zoom*k, -zoom, zoom)
            else:
                box = (-zoom, zoom, -zoom/k, zoom/k)
            
            if reg.proj == 'ortho':
                glOrtho(*box, self.view[4], self.view[5])
            else:
                glFrustum(*box, self.view[4], self.view[5])
            
            gluLookAt(*lookat,)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glScale(reg.scale, reg.scale, reg.scale)
            glTranslate(*reg.translate,)
            
            for name in reg.models:
                if reg.models[name]['display'] and (reg.models[name]['slide'] is None or reg.models[name]['slide'](self.sys_n)):
                    for item in reg.models[name]['component']:
                        if 'order' in item:
                            glPushMatrix()
                            if item['order'] in ('R', 'RT'):
                                phi, vec = item['rotate'](self.sys_n)
                                glRotatef(phi, *vec)
                                if item['order'] == 'RT':
                                    dx, dy, dz = item['translate'](self.sys_n)
                                    glTranslate(dx, dy, dz)
                            elif item['order'] in ('T', 'TR'):
                                dx, dy, dz = item['translate'](self.sys_n)
                                glTranslate(dx, dy, dz)
                                if item['order'] == 'TR':
                                    phi, vec = item['rotate'](self.sys_n)
                                    glRotatef(phi, *vec)
                        
                        if item['genre'] in ('surface', 'mesh'):
                            vid, eid, v_type, gl_type, texture = item['vars']
                            if 'light' in item or 'fill' in item:
                                glPushAttrib(GL_ALL_ATTRIB_BITS)
                                if 'light' in item:
                                    f1 = 1 + np.log(pow(reg.scale, 1/4)) if reg.scale > 1 else pow(reg.scale, 1/3)
                                    f2 = 1 + np.log(pow(reg.scale, 2)) if reg.scale > 1 else pow(reg.scale, 1/1.1)
                                    
                                    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.7*f1, 0.7*f1, 0.7*f1, 1.0))
                                    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.7*f2, 0.7*f2, 0.7*f2, 1.0))
                                    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.2*f1, 0.2*f1, 0.2*f1, 1.0))
                                    
                                    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.4*f1, 0.4*f1, 0.4*f1, 1.0))
                                    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.3*f2, 0.3*f2, 0.3*f2, 1.0))
                                    glLightfv(GL_LIGHT1, GL_SPECULAR, (0.2*f1, 0.2*f1, 0.2*f1, 1.0))
                                    
                                    glLightfv(GL_LIGHT2, GL_AMBIENT, (0.4*f1, 0.4*f1, 0.4*f1, 1.0))
                                    glLightfv(GL_LIGHT2, GL_DIFFUSE, (0.3*f2, 0.3*f2, 0.3*f2, 1.0))
                                    glLightfv(GL_LIGHT2, GL_SPECULAR, (0.2*f1, 0.2*f1, 0.2*f1, 1.0))
                                    
                                    glLightfv(GL_LIGHT3, GL_AMBIENT, (0.4*f1, 0.4*f1, 0.4*f1, 1.0))
                                    glLightfv(GL_LIGHT3, GL_DIFFUSE, (0.3*f2, 0.3*f2, 0.3*f2, 1.0))
                                    glLightfv(GL_LIGHT3, GL_SPECULAR, (0.2*f1, 0.2*f1, 0.2*f1, 1.0))
                                    
                                    glEnable(GL_LIGHTING)
                                    if item['light']%2 == 1:
                                        glEnable(GL_LIGHT0)
                                    if (item['light']>>1)%2 == 1:
                                        glEnable(GL_LIGHT1)
                                    if (item['light']>>2)%2 == 1:
                                        glEnable(GL_LIGHT2)
                                    if (item['light']>>3)%2 == 1:
                                        glEnable(GL_LIGHT3)
                                if 'fill' in item:
                                    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                            self._wxglDrawElements(reg, (vid, eid, v_type, gl_type, texture))
                            if 'light' in item or 'fill' in item:
                                glPopAttrib()
                        elif item['genre'] == 'line':
                            vid, eid, v_type, gl_type, width, stipple = item['vars']
                            if width or stipple:
                                glPushAttrib(GL_LINE_BIT)
                                if width:
                                    glLineWidth(width)
                                if stipple:
                                    glEnable(GL_LINE_STIPPLE)
                                    glLineStipple(*stipple,)
                            self._wxglDrawElements(reg, (vid, eid, v_type, gl_type, None))
                            if width or stipple:
                                glPopAttrib()
                        elif item['genre'] == 'point':
                            vid, eid, v_type, gl_type, size = item['vars']
                            if size:
                                glPushAttrib(GL_POINT_BIT)
                                glPointSize(size)
                            self._wxglDrawElements(reg, (vid, eid, v_type, gl_type, None))
                            if size:
                                glPopAttrib()
                        elif item['genre'] == 'text':
                            self._wxglDrawPixels(reg, item['vars'])
                        
                        if 'order' in item:
                            glPopMatrix()
        
    def repaint(self):
        """重绘"""
        
        self.SetCurrent(self.context)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)    # 清除屏幕及深度缓存
        self._draw_gl()                                     # 绘图
        self.SwapBuffers()                                  # 切换缓冲区，以显示绘制内容
    
    def set_proj(self, proj):
        """设置投影模式"""
        
        self.proj = proj
        for reg in self.regions:
            reg.proj = proj
    
    def set_mode(self, mode):
        """设置2D/3D模式"""
        
        self.mode = mode
    
    def set_style(self, style):
        """设置风格（背景和文本颜色）"""
        
        self.style = self._set_style(style)
        self._init_gl()
    
    def set_posture(self, oecs=None, zoom=None, dist=None, azimuth=None, elevation=None, save=False):
        """设置观察姿态（距离、方位角和仰角）
        
        oecs        - ECS原点
        zoom        - 视口缩放因子
        dist        - 眼睛与ECS原点的距离
        azimuth     - 方位角(度)
        elevation   - 仰角(度)
        save        - 是否保存当前设置，默认不保存
        """
        
        if not oecs is None:
            self.oecs = np.array(oecs)
        if not zoom is None:
            self.zoom = zoom
        if not dist is None:
            self.dist = dist
        if not azimuth is None:
            self.azimuth = azimuth
        if not elevation is None:
            self.elevation = elevation
        
        self._set_eye_and_up(save=save)
        self.update_grid()
        self.Refresh(False)
        
    def restore_posture(self):
        """还原观察姿态"""
        
        self.set_posture(**self.store)
        
    def get_scene_buffer(self, alpha=True, buffer='FRONT', crop=False):
        """以PIL对象的格式返回场景缓冲区数据
        
        alpha       - 是否使用透明通道
        buffer      - 显示缓冲区。默认使用前缓冲区（当前显示内容）
        crop        - 是否将宽高裁切为16的倍数
        """
        
        if alpha:
            gl_mode = GL_RGBA
            pil_mode = 'RGBA'
        else:
            gl_mode = GL_RGB
            pil_mode = 'RGB'
        
        if buffer == 'FRONT':
            glReadBuffer(GL_FRONT)
        elif buffer == 'BACK':
            glReadBuffer(GL_BACK)
        
        data = glReadPixels(0, 0, self.size[0], self.size[1], gl_mode, GL_UNSIGNED_BYTE, outputType=None)
        im = Image.fromarray(data.reshape(data.shape[1], data.shape[0], -1), mode=pil_mode)
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
        
        if crop:
            w, h = im.size
            nw, nh = 16*(w//16), 16*(h//16)
            x0, y0 = (w-nw)//2, (h-nh)//2
            x1, y1 = x0+nw, y0+nh
            im = im.crop((x0, y0, x1, y1))
        
        return im
        
    def save_scene(self, fn, alpha=True, buffer='FRONT', crop=False):
        """保存场景为图像文件
        
        fn          - 保存的文件名
        alpha       - 是否使用透明通道
        buffer      - 显示缓冲区。默认使用前缓冲区（当前显示内容）
        crop        - 是否将宽高裁切为16的倍数
        """
        
        im = self.get_scene_buffer(alpha=alpha, buffer=buffer, crop=crop)
        im.save(fn)
        
    def start_sys_timer(self):
        """启动模型几何变换定时器"""
        
        self.sys_timer.Stop()
        self.sys_n = 0
        self.sys_timer.Start(self.interval)
    
    def pause_sys_timer(self):
        """暂停/重启模型定时器"""
        
        if self.sys_timer.IsRunning():
            self.sys_timer.Stop()
        else:
            self.sys_timer.Start(self.interval)
    
    def get_font_list(self):
        """返回当前系统可用字体列表"""
        
        return self.fm.get_font_list
    
    def get_default_font(self):
        """返回默认字体"""
        
        return self.fm.default_font
    
    def set_default_font(self, font_name):
        """设置默认字体"""
        
        self.fm.set_default_font(font_name)
    
    def get_color_list(self):
        """返回颜色列表"""
        
        return self.cm.color_list
    
    def get_cmap_list(self):
        """返回调色板列表"""
        
        return self.cm.cmap_list
    
    def get_color_help(self):
        """返回颜色中英文对照表"""
        
        return self.cm.color_help()
    
    def get_cmap_help(self):
        """返回调色板分类列表"""
        
        return self.cm.cmap_help()
    
    def add_region(self, box, fixed=False, proj=None):
        """添加视区
        
        box         - 四元组，元素值域[0,1]。四个元素分别表示视区左下角坐标、宽度、高度
        fixed       - 布尔型，是否锁定旋转缩放
        proj        - 投影模式
                        None        - 使用场景对象的投影模式
                        'ortho'     - 平行投影
                        'cone'      - 透视投影
        """
        
        if proj is None:
            proj = self.proj
        
        reg = region.WxGLRegion(self, box, fixed, proj)
        self.regions.append(reg)
        
        return reg
    
        