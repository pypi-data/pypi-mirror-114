from typing import Any, Callable

import ipywidgets as widgets
from ipywidgets import Button, ButtonStyle, GridBox, Layout, Textarea, VBox

from antannotator.persistence import AnnotationEvent, AnnotationSample


def get_text_classification_wiget(sample:AnnotationSample, on_done: Callable[[Any],None], show_comment=True):
    def get_option(text):
        return widgets.ToggleButton(
                value=False,
                description=text,
                disabled=False,
                layout=Layout(height="40px")
                #button_style='', # 'success', 'info', 'warning', 'danger' or ''
                #tooltip='Description',
                #icon='check' # (FontAwesome names without the `fa-` prefix)
            )

    available_options = sample.available_options
    
    options_dict = dict([(key, get_option(text))  for (key, text) in available_options.items()])

    options = VBox(list(options_dict.values()), layout=Layout(width='auto', grid_area='options', min_height="300px"))

    
    task  = Textarea(value=sample.task_data,
                    layout=Layout(width='auto', grid_area='task', align_items="stretch"),# height="500px"
                    disabled=True)

    # TODO show sample.visible_info in info


    comment = Textarea(value='',
                placeholder='Comment',
                description='',
                disabled=False,
                layout=Layout( grid_area='comment'))

    done_button = Button(description='Done', button_style="success")

    def on_done_clicked(change):
        annotation_result = {
            "selected_options": [ {"key": key, "description": available_options[key]} for key, button in options_dict.items() if button.value == True],
            "comment": (comment.value if show_comment else None)}
        on_done(annotation_result)

    done_button.on_click(on_done_clicked)
    
    control = VBox([done_button] , layout=Layout(width='auto', grid_area='control'))

    info = VBox([] , layout=Layout(width='auto', grid_area='info', min_height="70px"))

    
    


    all_items = []
    all_items.append(task)
    all_items.append(options)
    all_items.append(control)
    all_items.append(info)
    if show_comment:
        all_items.append(comment)


    return GridBox(children=all_items,
            layout=Layout(
                width='1500px',
                grid_gap='5px 10px',
                grid_template_rows='auto auto auto auto 20px 90px',
                grid_template_columns='25% 25% 25% 25%',
                grid_template_areas='''
                "task task task info"
                "task task task options"
                "task task task options"
                "task task task comment"
                "task task task space"            
                "task task task control"
                ''')
        )
