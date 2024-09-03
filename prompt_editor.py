import marimo

__generated_with = "0.8.7"
app = marimo.App(width="medium", app_title="Prompt Editor")


@app.cell
def __(mo):
    mo.md(r"""# Prompt Editor""")
    return


@app.cell
def __():
    import marimo as mo
    import json

    fn = "lang_config.json"
    with open(fn, "r") as f:
        d = json.load(f)
    return d, f, fn, json, mo


@app.cell
def __(d, mo):
    sel_lang = mo.ui.radio(options=list(d.keys()), value=list(d.keys())[0], label="Choose configuration to modify")
    sel_lang
    return sel_lang,


@app.cell
def __(d, mo, sel_lang):
    inp_sys = mo.ui.text_area(d[sel_lang.value]['system_prompt'], label="Edit system prompt", full_width=True)
    inp_sys
    return inp_sys,


@app.cell
def __(d, mo, sel_lang):
    inp_msg = mo.ui.text_area(d[sel_lang.value]['starting_message'], label="Edit starting message", full_width=True)
    inp_msg
    return inp_msg,


@app.cell
def __(d, fn, inp_msg, inp_sys, json, mo, sel_lang):
    def modify_json():
        d[sel_lang.value] = {
            "system_prompt": inp_sys.value,
            "starting_message": inp_msg.value
        }
        with open(fn, "w") as f:
            json.dump(d)

    save_edits = mo.ui.button(on_click=modify_json, label="Save modified prompt")
    save_edits
    return modify_json, save_edits


@app.cell
def __():
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
