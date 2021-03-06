# -*- coding: utf-8 -*-
"""Easy Text Summarization with BART.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/BritneyMuller/colab-notebooks/blob/master/Easy_Text_Summarization_with_BART.ipynb

# BART (a new Seq2Seq model with SoTA summarization performance) that runs from colab with Javascript UI

> [Original Colab and article by Sam Shleifer](https://github.com/sshleifer/blog_v2/blob/master/_notebooks/2020-03-12-bart.ipynb)

> [JavaScript UI in Colab idea](https://github.com/gpt2ent/gpt2colab-js)


**STEPS:**

1. Runtime -> Reset all runtimes
2. Runtime -> Run all
3. Scroll down and wait until you see the little window with a from
5. Type text the text to be summarized and click on **Summarize** button
6. After a while, the summary will be shown in the form and downloaded!
"""

!git clone https://github.com/huggingface/transformers \
&& cd transformers \

!pip install -q ./transformers

import torch
import transformers
from transformers import BartTokenizer, BartForConditionalGeneration

tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

#torch_device = 'cuda' if torch.cuda.is_available() else 'cpu '# failing when device is gpu
torch_device = 'cpu'

import google.colab.output

def bart_summarize(text, num_beams, length_penalty, max_length, min_length, no_repeat_ngram_size):
  
  text = text.replace('\n','')
  text_input_ids = tokenizer.batch_encode_plus([text], return_tensors='pt', max_length=1024)['input_ids'].to(torch_device)
  summary_ids = model.generate(text_input_ids, num_beams=int(num_beams), length_penalty=float(length_penalty), max_length=int(max_length), min_length=int(min_length), no_repeat_ngram_size=int(no_repeat_ngram_size))           
  summary_txt = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
  return summary_txt

#register callback for Javascript
google.colab.output.register_callback('bart_summarize', bart_summarize)

from IPython.display import HTML

#spinner from https://codepen.io/vovchisko/pen/vROoYQ
spinner_css = """
<style>
@keyframes c-inline-spinner-kf {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.c-inline-spinner,
.c-inline-spinner:before {
  display: inline-block;
  width: 11px;
  height: 11px;
  transform-origin: 50%;
  border: 2px solid transparent;
  border-color: #74a8d0 #74a8d0 transparent transparent;
  border-radius: 50%;
  content: "";
  animation: linear c-inline-spinner-kf 300ms infinite;
  position: relative;
  vertical-align: inherit;
  line-height: inherit;
}
.c-inline-spinner {
  top: 3px;
  margin: 0 3px;
}
.c-inline-spinner:before {
  border-color: #74a8d0 #74a8d0 transparent transparent;
  position: absolute;
  left: -2px;
  top: -2px;
  border-style: solid;
}
</style>
"""

input_form = """
<link rel="stylesheet" href="https://unpkg.com/purecss@1.0.1/build/pure-min.css" integrity="sha384-oAOxQR6DkCoMliIh8yFnu25d7Eq/PHS21PClpwjOTeU2jRSq11vu66rf90/cZr47" crossorigin="anonymous">

<div style="background-color:white; border:solid #ccc; width:800px; padding:20px; color: black;">
<p><strong>BART</strong> Seq2Seq model with SoTA summarization performance</p>
<textarea id="main_textarea" cols="75" rows="20" placeholder="Paste your text here..." style="font-family: 'Liberation Serif', 'DejaVu Serif', Georgia, 'Times New Roman', Times, serif; font-size: 13pt; padding:10px;"></textarea><br>
<div class="pure-form pure-form-aligned">
   <div class="pure-control-group">
     <label for="no_repeat_ngram_size"><strong>no_repeat_ngram_size:</strong></label>
     <input type="number" id="no_repeat_ngram_size" value="3" style="background-color: white;">
    </div>
    <div class="pure-control-group">
      <label for="num_beams"><strong>num_beams:</strong></label>
      <input type="number" min="0" max="10" step="1" id="num_beams" value="4" style="background-color: white;">
    </div>
    <div class="pure-control-group">
        <label for="length_penalty"><strong>length_penalty:</strong></label>
        <input type="number" min="0.0" max="10.0" step="0.1" id="length_penalty" value="2.0" style="background-color: white;">
    </div>
    <div class="pure-control-group">
        <label for="max_length"><strong>max_length:</strong></label>
        <input type="number" id="max_length" value="142" style="background-color: white;">
    </div>
     <div class="pure-control-group">
        <label for="min_length"><strong>min_length:</strong></label>
        <input type="number" id="min_length" value="56" style="background-color: white;">
    </div>
    <p><a target="_blank" href='https://pastebin.com/raw/BMPcUS6v'>Try to summarize this example article</a></p>
    <div style="width: 300px; display: block; margin-left: auto !important; margin-right: auto !important;">
        <p><button class="pure-button pure-button-primary" style="font-size: 125%%;" onclick="summarize()">Summarize</button>
        <span class="c-inline-spinner" style="visibility: hidden;" id="spinner"></span></p>
    </div>
</div>
</div>
"""

javascript = """
<script type="text/Javascript">


       function saveTextAsFile(textToWrite, fileNameToSaveAs)
    {
    	var textFileAsBlob = new Blob([textToWrite], {type:'text/plain'}); 
    	var downloadLink = document.createElement("a");
    	downloadLink.download = fileNameToSaveAs;
    	downloadLink.innerHTML = "Download File";
    	if (window.webkitURL != null)
    	{
    		// Chrome allows the link to be clicked
    		// without actually adding it to the DOM.
    		downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
    	}
    	else
    	{
    		// Firefox requires the link to be added to the DOM
    		// before it can be clicked.
    		downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
    		downloadLink.onclick = destroyClickedElement;
    		downloadLink.style.display = "none";
    		document.body.appendChild(downloadLink);
    	}
    
    	downloadLink.click();
    }


    function summarize(){
        
        var text = document.getElementById('main_textarea').value;
        var no_repeat_ngram_size = document.getElementById('no_repeat_ngram_size').value;
        var num_beams = document.getElementById('num_beams').value;
        var length_penalty = document.getElementById('length_penalty').value;
        var max_length = document.getElementById('max_length').value;
        var min_length = document.getElementById('min_length').value;
        
        var kernel = google.colab.kernel;

        var resultPromise = kernel.invokeFunction("bart_summarize", [text,num_beams,length_penalty,max_length,min_length,no_repeat_ngram_size]); // developer, look here
        resultPromise.then(
            function(result) {
              document.getElementById('main_textarea').value = 'da resultado';
              document.getElementById('main_textarea').value = result.data["text/plain"];
              document.getElementById('spinner').style = "visibility: hidden;";
              saveTextAsFile(result.data["text/plain"], 'summary.txt')
        }).catch(function(error){document.getElementById('main_textarea').value = error;});
        document.getElementById('spinner').style = "visibility: visible;";
    };
</script>
""" 


HTML(spinner_css + input_form + javascript)

