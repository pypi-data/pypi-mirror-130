from IPython.core.display import display, HTML, Markdown
def hr(): display(HTML('<hr/>'))
def heading(n, title): display(HTML(f'<h{n}>{title}</h{n}>'))
def h1(title): heading(1, title)
def h2(title): hr(); heading(2, title)
def h3(title): heading(3, title)
def paragraph(content): display(HTML(f'<p>{content}</p>'))
