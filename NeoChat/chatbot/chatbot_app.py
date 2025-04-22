from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import gradio as gr

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Chat function
def chat(input_text, chat_history_ids=None):
    new_input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors ='pt')

    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=1)
    else:
        bot_input_ids = new_input_ids

        chat_history_ids = model.generate(
            bot_input_ids,
            max_length =1000,
            pad_token_id = tokenizer.eos_token_id,
            no_repeat_ngram_size = 3,
            do_sample =True,
            top_k =100,
            top_p = 0.7,
            temperature =0.8
        )

        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens = True)
        return response, chat_history_ids


def respond(message, chat_history):
    bot_message, _ = chat(message)
    chat_history.append((message, bot_message))
    return "", chat_history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()


