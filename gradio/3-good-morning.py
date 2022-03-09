import gradio as gr


def greet(name, is_morning, temperature):
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = "%s %s. It is %s degrees today" % (salutation, name, temperature)
    celsius = (temperature - 32) * 5 / 9
    return greeting, round(celsius, 2)


iface = gr.Interface(
    fn=greet,
    inputs=["text", "checkbox", gr.inputs.Slider(0, 100)],
    outputs=["text", "number"],
)
iface.launch()