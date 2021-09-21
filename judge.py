import yaml,os,logger,sys,shutil,subprocess
CUR_RUN_ID=1
CUR_PATH=os.path.abspath(os.path.dirname(__file__))
os.chdir(CUR_PATH)
LANGUAGE_FOLDER_PATH=os.path.join(CUR_PATH,"langs")
EXCUTE_FOLDER_PATH=os.path.join(CUR_PATH,"running")
PROBLEM_FOLDER_PATH=os.path.join(CUR_PATH,"problems")
if(not os.path.exists(LANGUAGE_FOLDER_PATH)):
    logger.log('language dir not exists...creating')
    os.mkdir('langs')
    logger.log("created language dir 'langs'")

# 清空运行缓存
if(os.path.exists(EXCUTE_FOLDER_PATH)):shutil.rmtree('running')
os.mkdir('running')
if(not os.path.exists(PROBLEM_FOLDER_PATH)):os.mkdir('problems')

langsdir=os.listdir(LANGUAGE_FOLDER_PATH)
logger.log("scaned %d files in the langs folder, checking"%len(langsdir))
logger.log("files: %s"% ",".join(langsdir))
LANGUAGES={}
# It may look like this:
# {
#     "C++":{# from the "language_name" field of yml
#         compile:"g++ xxx -o xxx"
#         run:"xxx < in >out" # windows
#     }
# }
for filename in langsdir:
    if(os.path.splitext(filename)[1].lower()=='.yml'):
        with open(os.path.join(LANGUAGE_FOLDER_PATH,filename),encoding="utf-8")as fp:
            data=yaml.load(fp,Loader=yaml.FullLoader)
            if(not data):
                logger.warning("failed to load the file langs/%s, will ignore it"%filename)
                continue
            if(not data.get("language_name")):
                logger.warning("The key 'language_name' is not defined in the file langs/%s, will ignore this language"%filename)
                continue
            if(not data.get("run_command_windows")):
                logger.warning("The key 'run_command_windows' is not defined in the file langs/%s, will ignore this language"%filename)
                continue
            if(not data.get("run_command_linux")):
                logger.warning("The key 'run_command_linux' is not defined in the file langs/%s, will ignore this language"%filename)
                continue
            if(not data.get("compile_command_windows")):
                logger.warning("The key 'compile_command_windows' is not defined in the file langs/%s, will ignore this language"%filename)
                continue
            if(not data.get("compile_command_linux")):
                logger.warning("The key 'compile_command_linux' is not defined in the file langs/%s, will ignore this language"%filename)
                continue
            logger.log('loading language langs/%s'%filename)
            run_script=""
            compile_script=""
            if("linux" in sys.platform):
                run_script=data.get("run_command_linux")
                compile_script=data.get("compile_command_linux")
            elif("win" in sys.platform):
                run_script=data.get("run_command_windows")
                compile_script=data.get("compile_command_windows")
            LANGUAGES[data["language_name"]]={
                "run":run_script,
                "compile":compile_script
            }
            logger.log('loaded language langs/%s'%filename)
logger.log('languages load finished: %d languages'%len(LANGUAGES))
logger.log(LANGUAGES)
def compileLang(file,lang,folder):
    lang_profile=LANGUAGES[lang]
    compile_p=subprocess.Popen(lang_profile["compile"].format(dir=folder,filename=file),shell=True)
    if(compile_p.wait()!=0):
        return {'status':"CE"}
    return {'status':'!CE'}
def runLang(lang,folder,input_file,output_file,compare_output_file):
    lang_profile=LANGUAGES[lang]
    print(folder)
    print(lang_profile["run"].format(dir=folder,output=output_file,input=input_file))
    run_p=subprocess.Popen(lang_profile["run"].format(dir=folder,output=output_file,input=input_file),shell=True)
    if(run_p.wait()!=0):
        return {'status':"RE"}
    with open(output_file,encoding="utf-8")as fp:
        user_res=fp.read()
    with open(compare_output_file,encoding="utf-8")as fp:
        std_res=fp.read()
        if(user_res==std_res):
            return {'status':"AC"}
        else:
            return {'status':'WA'}
def judge(problem_name,filename,lang,folder):
    problem_path=os.path.join(PROBLEM_FOLDER_PATH,problem_name)
    points={}
    for i in os.listdir(problem_path):
        spt=os.path.splitext(i)
        if(spt[1]==".in"):
            if(not points.get(spt[0])):
                points[spt[0]]={'in':i}
            else:
                points[spt[0]]["in"]=i
        elif(spt[1]==".out"):
            if(not points.get(spt[0])):
                points[spt[0]]={'out':i}
            else:
                points[spt[0]]["out"]=i
    logger.log(problem_name)
    logger.log(points)
    ret=compileLang(filename,lang,folder)
    if(ret['status']=='CE'):
        return 0,['CE']
    score_list=[]
    score=0
    perscore=100/len(points)
    for i in points:
        stat=runLang(lang,folder,os.path.join(problem_path,points[i]['in']),os.path.join(problem_path,"fileoutput.out"),os.path.join(problem_path,points[i]['out']))
        score_list.append(stat['status'])
        if(stat['status']=='AC'):
            score+=perscore
    return score,score_list
def create_run(problem):
    global CUR_RUN_ID
    me=CUR_RUN_ID
    CUR_RUN_ID+=1
    os.chdir(EXCUTE_FOLDER_PATH)
    os.mkdir(str(me))
    os.chdir(CUR_PATH)
    shutil.copyfile('test.cpp',f'running/{me}/file.cpp')
    with open(f'running/{me}/problem','w')as fp:
        fp.write(problem)
    score,l=judge(problem,os.path.join(EXCUTE_FOLDER_PATH,f'{me}/file.cpp'),'C++',os.path.join(EXCUTE_FOLDER_PATH,f'{me}'))
    print(score,l)
create_run("P1000 Hello World")