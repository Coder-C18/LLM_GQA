
<h1>Pipe Line Q&A Document use LLM</h1>
<p> I implement pipeline product following :
</p>
<img src="https://raw.githubusercontent.com/Coder-C18/LLM_GQA/main/images/pipe line.jpg">


<h1> Install Qdrant Database</h1>


<h2>Requirement</h2>
* ### LLM : Gemini
* ### Vector Database :qdrant
* ### Python : >3.8



# Install Qdrant using docker
```commandline
docker pull qdrant/qdrant
```
```commandline
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```
<h1> Documentation</h1>
Clone repo and install requirements.txt in a Python>=3.8.0 environment

```commandline
pip install -r requirements.txt
```
```commandline
python GUI.py
```

