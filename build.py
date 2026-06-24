def get_personal_data():
    name = ["Minyang", "Li"]
    email = "mli861@connect.hkust-gz.edu.cn"
    bio_text = f"""
                <p>
                    I am an undergraduate student in Artificial Intelligence at
                    <a href="https://www.hkust-gz.edu.cn/" target="_blank">The Hong Kong University of Science and Technology (Guangzhou)</a>, supervised by <a href="https://www.yingcong.me/" target="_blank">Prof. Ying-Cong Chen</a>.
                    I have spent wonderful times collabrating with <a href="https://scholar.google.com/citations?user=Vm1moSIAAAAJ&hl=en" target="_blank">Zhen Yang</a> in Prof. Chen's lab.
                    I was also privileged to be supervised by <a href="https://scholar.google.com/citations?user=kSU8IiQAAAAJ&hl=en" target="_blank">Dr. Qichun Yang</a> at the begining of my research journey.
                    My research interests center on computer vision and visual generative models, with a primary focus on
diffusion models. I am also interested in their connections to embodied AI, including Vision-Language-
Action (VLA) systems, diffusion models for decision making, and RL-based preference optimization for
diffusion models and VLMs
                </p>
                <p>
                    <a href="cv_4%20(4).pdf" target="_blank" style="margin-right: 5px"><i class="fa fa-address-card fa-lg"></i> CV</a>
                    <span style="margin-right: 5px"><i class="far fa-envelope-open fa-lg"></i> {email}</span>
                    <a href="https://scholar.google.com/citations?user=iahnRcgAAAAJ&hl=zh-CN" target="_blank" style="margin-right: 5px"><i class="fa-solid fa-book"></i> Scholar</a>
                </p>
    """
    footer = """
            <div class="col-sm-12" style="">
                <h4>Homepage Template</h4>
                <p>
                    This homepage is adapted from the open-source
                    <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">m-niemeyer/m-niemeyer.github.io</a>
                    academic homepage template.
                </p>
            </div>
    """
    return name, bio_text, footer

def get_author_dict():
    return {
        'Ying-Cong Chen': 'https://www.hkust-gz.edu.cn/',
        'Qichun Yang': 'https://www.hkust-gz.edu.cn/',
    }

def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name='Minyang Li', add_links=True):
    links = get_author_dict() if add_links else {}
    s = ""
    for p in persons:
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('last'): 
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        if string_part_i in links.keys():
            string_part_i = f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}</a>'
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span style="font-weight: bold";>{make_bold_name}</span>'
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_paper_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""

    if 'html' in entry.fields.keys() and entry.fields['html'] != '#':
        title = f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a>"""
    else:
        title = entry.fields['title']

    if 'award' in entry.fields.keys():
        s += f"""{title} <span style="color: red;">({entry.fields['award']})</span><br>"""
    else:
        s += f"""{title} <br>"""

    s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'html': 'Project Page', 'pdf': 'Paper', 'supp': 'Supplemental', 'video': 'Video', 'poster': 'Poster', 'code': 'Code'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if k == 'html' and entry.fields[k] == '#':
                continue
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1

    cite = "<pre><code>@InProceedings{" + f"{entry_key}, \n"
    cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
    for entr in ['title', 'booktitle', 'year']:
        cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</pre></code>"""
    s += " /" + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapseExample" style="margin-left: -6px; margin-top: -2px;">Expand bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    s += """ </div> </div> </div>"""
    return s

def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    s += f"""{entry.fields['title']}<br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'slides': 'Slides', 'video': 'Recording'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    s += """ </div> </div> </div>"""
    return s

def get_publications_html():
    publications = [
        {
            'title': 'RectifiedHR: Enable Efficient High-Resolution Synthesis via Energy Rectification',
            'authors': 'Zhen Yang*, Guibao Shen*, <span style="font-weight: bold;">Minyang Li*</span>, Liang Hou, Mushui Liu, Luozhou Wang, Xin Tao, and Ying-Cong Chen',
            'venue': 'CVPR Findings',
            'year': '2026',
            'img': 'assets/img/publications/Screenshot 2026-06-08 at 11.38.04.png',
            'pdf': 'https://openaccess.thecvf.com/content/CVPR2026F/papers/Yang_RectifiedHR_Enable_Efficient_High-Resolution_Synthesis_via_Energy_Rectification_CVPRF_2026_paper.pdf',
        },
        {
            'title': 'Future Climate Change Increases Streamflow and Risks of Hydrological Hazards in the Pearl River Basin',
            'authors': 'Haoyuan Yu, Qichun Yang, Liuqian Yu, Xia Li, <span style="font-weight: bold;">Minyang Li</span>, and Yingxian Yang',
            'venue': 'Water',
            'year': '2026',
            'img': 'assets/img/publications/Screenshot 2026-06-08 at 11.38.22.png',
            'pdf': 'https://sciprofiles.com/publication/view/d60a42132a66345cf41ba02e72aa2119',
        },
    ]
    s = ""
    for publication in publications:
        s += f"""
            <div style="margin-bottom: 3em;">
                <div class="row">
                    <div class="col-sm-3">
                        <img src="{publication['img']}" class="img-fluid img-thumbnail" alt="Project image">
                    </div>
                    <div class="col-sm-9">
                        {publication['title']}<br>
                        {publication['authors']}<br>
                        <span style="font-style: italic;">{publication['venue']}</span>, {publication['year']}<br>
                        <a href="{publication['pdf']}" target="_blank">PDF</a>
                    </div>
                </div>
            </div>
        """
    return s

def get_talks_html():
    return ""

def get_education_html():
    return """
        <div style="margin-bottom: 2em;">
            <span style="font-weight: bold;">The Hong Kong University of Science and Technology (Guangzhou)</span>
            <span style="float: right;">Sep. 2023 - Jun. 2027 (expected)</span><br>
            B.E. in Artificial Intelligence.
        </div>
        <div style="margin-bottom: 2em;">
            <span style="font-weight: bold;">National University of Singapore</span>
            <span style="float: right;">Jun. 2026 - Jul. 2026</span><br>
            Exchange student.
        </div>
    """

def get_research_html():
    return """
        <div style="margin-bottom: 2em;">
            <span style="font-weight: bold;">AI Researcher (Algorithm Intern)</span>
            <span style="float: right;">Mar. 2026 - Present</span><br>
            Mentor: <a href="https://ieeexplore.ieee.org/author/37086305237" target="_blank">Dr. Tianyi Zhang</a><br>
            <a href="https://knowinai.com/" target="_blank">Knowin AI</a>, Nanshan, Shenzhen, China
        </div>
    """

def get_projects_html():
    return """
        <div style="margin-bottom: 2em;">
            <span style="font-weight: bold;">Multi-Object Image Editing</span><br>
            <span style="font-style: italic;">Independent, Course Project in Deep Learning</span><br>
            Proposed VGFE, an inversion-free flow-based image editing framework that uses VQA-guided editing strength search to automatically select optimal edit strength while reducing computational overhead.
            Extended the method to multi-object editing by designing a reassembly and re-editing pipeline tailored for inversion-free diffusion/flow models.
            (<a href="https://drive.google.com/file/d/1i1UlNpWH-OpHx7uIAk3uxUgMi0ek5Ehb/view?usp=sharing" target="_blank">Report</a>)
        </div>
        <div style="margin-bottom: 2em;">
            <span style="font-weight: bold;">Skeleton-Adhered Style Transfer for Chinese Characters</span><br>
            <span style="font-style: italic;">Collaborator: Jian Yang, Course Project in CompTec for Sketch-based Creativity</span><br>
            Developed CalliGen, a sketch-based Chinese calligraphy generation system that transforms rough handwritten skeletons into stylized calligraphic characters while preserving users' structural intent.
            Designed an efficient pipeline to construct a large-scale paired dataset of Chinese character images and skeletons for training.
            Co-designed an interactive prototype supporting sketch editing, style selection, and real-time generation.
            (<a href="https://drive.google.com/file/d/18R5_xT_vy4KYV7v_KD1ehNGC0PfeRrCm/view?usp=sharing" target="_blank">Report</a>)
            (<a href="https://github.com/MinyangLi/CalliGen" target="_blank">Code</a>)
            (<a href="https://drive.google.com/file/d/1iQRfb1LKmFFCS4X1nILYP2oTv_eOPs8E/view?usp=sharing" target="_blank">Demo video</a>)
        </div>
        <div style="margin-bottom: 2em;">
            <span style="font-weight: bold;">Fact-Aware Consistency Scoring for Model-Generated Answers</span><br>
            <span style="font-style: italic;">Collaborator: <a href="https://cozy000000.github.io/" target="_blank">Zhiyi Chen</a>, Zhiling Li, Course Project in Intro2NLP</span><br>
            To address the limitations of global embedding similarity in detecting entity, date, number, and span-level errors, we proposed FS-BGE, a BGE-M3 ColBERT-based similarity score with factual token reweighting and answer-span mismatch penalties, and I further explored bidirectional NLI-based entailment scoring and scoring in hyperbolic space.
            (<a href="https://drive.google.com/file/d/1FaRJxWKnEG81mTCiP8CgtOgxh89Ikwip/view?usp=sharing" target="_blank">Report</a>)
            (<a href="https://github.com/MinyangLi/nlp_project" target="_blank">Code</a>)
        </div>
    """

def get_index_html():
    pub = get_publications_html()
    education = get_education_html()
    research = get_research_html()
    projects = get_projects_html()
    name, bio_text, footer = get_personal_data()
    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <title>{name[0] + ' ' + name[1]}</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
</head>

<body>
    <div class="container">
        <div class="row">
            <div class="col-md-1"></div>
            <div class="col-md-10">
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="margin-bottom: 1em;">
                    <h3 class="display-4" style="text-align: center;"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h3>
                    </div>
                    <br>
                    <div class="col-md-10" style="">
                        {bio_text}
                    </div>
                    <div class="col-md-2" style="">
                        <img src="assets/img/profile.jpg" class="img-thumbnail" width="280px" alt="Profile picture">
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>Education</h4>
                        {education}
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>Publications</h4>
                        {pub}
                    </div>
                </div>
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="">
                        <h4>Internship</h4>
                        {research}
                    </div>
                </div>
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="">
                        <h4>Selected Projects</h4>
                        {projects}
                    </div>
                </div>
                <div class="row" style="margin-top: 3em; margin-bottom: 1em;">
                    {footer}
                </div>
            </div>
            <div class="col-md-1"></div>
        </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
</body>

</html>
    """
    return s


def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w') as f:
        f.write(s)
    print(f'Written index content to {filename}.')

if __name__ == '__main__':
    write_index_html('index.html')
