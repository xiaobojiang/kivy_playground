from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics import RenderContext, Color, Rectangle, BindTexture

fs_multitexture='''
$HEADER$
uniform sampler2D texture1;
void main(void)
{
    gl_FragColor = frag_color * \
        texture2D(texture0, tex_coord0) * \
        texture2D(texture1, tex_coord0);
}
'''


kv = '''
<MultitextureLayout>
    Image:
        source: "mtexture1.png"
        size_hint: 0.3,0.3
        id: 1
        pos: 0,200
    Image:
        source: "mtexture2.png"
        size_hint: 0.3, 0.3
        id: 2
        pos: 200,200
    MultitextureWidget:
    
'''

Builder.load_string(kv)

class MultitextureWidget(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext()
        self.canvas.shader.fs = fs_multitexture
        with self.canvas:
            Color(1,1,1)
            BindTexture(source='mtexture2.png', index=1)
            Rectangle(size=(150,150), source='mtexture1.png', pos=(500,200))
        self.canvas['texture1'] = 1
        super(MultitextureWidget, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_glsl, 0)

    def update_glsl(self, *largs):
        self.canvas['projection_mat'] = Window.render_context['projection_mat']
        self.canvas['modelview_mat'] = Window.render_context['modelview_mat']

class MultitextureLayout(FloatLayout):
    def __init__(self, **kwargs):
        self.size = kwargs['size']
        super(MultitextureLayout,self).__init__(**kwargs)

class MultitextureApp(App):
    def build(self):
        return MultitextureLayout(size=(600,600))

if __name__ == '__main__':
    MultitextureApp().run()