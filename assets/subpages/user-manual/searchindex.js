Search.setIndex({docnames:["apidocs/hutts_verification","apidocs/hutts_verification.id_contexts","apidocs/hutts_verification.image_preprocessing","apidocs/hutts_verification.image_processing","apidocs/hutts_verification.utils","apidocs/hutts_verification.verification","apidocs/modules","faq","index","install","interface","introduction","requirements/install_docker","requirements/install_source","server"],envversion:53,filenames:["apidocs/hutts_verification.rst","apidocs/hutts_verification.id_contexts.rst","apidocs/hutts_verification.image_preprocessing.rst","apidocs/hutts_verification.image_processing.rst","apidocs/hutts_verification.utils.rst","apidocs/hutts_verification.verification.rst","apidocs/modules.rst","faq.rst","index.rst","install.rst","interface.rst","introduction.rst","requirements/install_docker.rst","requirements/install_source.rst","server.rst"],objects:{"":{hutts_verification:[0,0,0,"-"]},"hutts_verification.id_contexts":{id_context:[1,0,0,"-"],sa_id:[1,0,0,"-"],sa_id_book:[1,0,0,"-"],sa_id_book_old:[1,0,0,"-"],sa_id_card:[1,0,0,"-"],up_student_card:[1,0,0,"-"]},"hutts_verification.id_contexts.id_context":{FieldType:[1,1,1,""],IDContext:[1,1,1,""],LineType:[1,1,1,""]},"hutts_verification.id_contexts.id_context.FieldType":{DATE_HYPHENATED:[1,2,1,""],MIXED:[1,2,1,""],NUMERIC_ONLY:[1,2,1,""],TEXT_ONLY:[1,2,1,""]},"hutts_verification.id_contexts.id_context.IDContext":{get_id_info:[1,3,1,""]},"hutts_verification.id_contexts.id_context.LineType":{TITLED_ADJACENT:[1,2,1,""],TITLED_NEWLINE:[1,2,1,""],UNTITLED_ADJACENT:[1,2,1,""],UNTITLED_NEWLINE:[1,2,1,""]},"hutts_verification.id_contexts.sa_id":{SAID:[1,1,1,""]},"hutts_verification.id_contexts.sa_id.SAID":{MIN_AGE_DELTA:[1,2,1,""],POST_PROCESS_MIN_FUZZY_RATIO:[1,2,1,""],VALID_ID_LENGTH:[1,2,1,""],YEAR_DELTA:[1,2,1,""],validate_id_number:[1,3,1,""]},"hutts_verification.id_contexts.sa_id_book":{SAIDBook:[1,1,1,""]},"hutts_verification.id_contexts.sa_id_book_old":{SAIDBookOld:[1,1,1,""]},"hutts_verification.id_contexts.sa_id_card":{SAIDCard:[1,1,1,""]},"hutts_verification.id_contexts.up_student_card":{UPStudentCard:[1,1,1,""]},"hutts_verification.image_preprocessing":{blur_manager:[2,0,0,"-"],build_director:[2,0,0,"-"],color_manager:[2,0,0,"-"],face_manager:[2,0,0,"-"],pipeline:[2,0,0,"-"],pipeline_builder:[2,0,0,"-"],template_matching:[2,0,0,"-"],thresholding_manager:[2,0,0,"-"]},"hutts_verification.image_preprocessing.blur_manager":{BlurManager:[2,1,1,""]},"hutts_verification.image_preprocessing.blur_manager.BlurManager":{apply:[2,3,1,""],blur:[2,3,1,""],gaussianBlur:[2,3,1,""],medianBlur:[2,3,1,""]},"hutts_verification.image_preprocessing.build_director":{BuildDirector:[2,1,1,""]},"hutts_verification.image_preprocessing.build_director.BuildDirector":{construct_face_extract_pipeline:[2,4,1,""],construct_text_extract_pipeline:[2,4,1,""]},"hutts_verification.image_preprocessing.color_manager":{ColorManager:[2,1,1,""]},"hutts_verification.image_preprocessing.color_manager.ColorManager":{apply:[2,3,1,""],blackHat:[2,3,1,""],extractChannel:[2,3,1,""],histEqualisation:[2,4,1,""],topHat:[2,3,1,""]},"hutts_verification.image_preprocessing.face_manager":{FaceDetector:[2,1,1,""]},"hutts_verification.image_preprocessing.face_manager.FaceDetector":{blur_face:[2,3,1,""],detect:[2,3,1,""],extract_face:[2,3,1,""]},"hutts_verification.image_preprocessing.pipeline":{Pipeline:[2,1,1,""]},"hutts_verification.image_preprocessing.pipeline.Pipeline":{process_face_extraction:[2,3,1,""],process_text_extraction:[2,3,1,""]},"hutts_verification.image_preprocessing.pipeline_builder":{PipelineBuilder:[2,1,1,""]},"hutts_verification.image_preprocessing.pipeline_builder.PipelineBuilder":{get_result:[2,3,1,""],set_blur_manager:[2,3,1,""],set_color_manager:[2,3,1,""],set_face_detector:[2,3,1,""],set_threshold_manager:[2,3,1,""]},"hutts_verification.image_preprocessing.template_matching":{TemplateMatching:[2,1,1,""]},"hutts_verification.image_preprocessing.template_matching.TemplateMatching":{identify:[2,3,1,""]},"hutts_verification.image_preprocessing.thresholding_manager":{ThresholdingManager:[2,1,1,""]},"hutts_verification.image_preprocessing.thresholding_manager.ThresholdingManager":{adaptiveThresholding:[2,4,1,""],apply:[2,3,1,""],otsuThresholding:[2,4,1,""]},"hutts_verification.image_processing":{barcode_manager:[3,0,0,"-"],context_manager:[3,0,0,"-"],controllers:[3,0,0,"-"],sample_extract:[3,0,0,"-"],simplification_manager:[3,0,0,"-"],text_cleaner:[3,0,0,"-"]},"hutts_verification.image_processing.barcode_manager":{BarCodeManager:[3,1,1,""]},"hutts_verification.image_processing.barcode_manager.BarCodeManager":{apply_barcode_blur:[3,3,1,""],detect:[3,3,1,""],get_barcode_info:[3,3,1,""]},"hutts_verification.image_processing.context_manager":{ContextManager:[3,1,1,""]},"hutts_verification.image_processing.context_manager.ContextManager":{get_id_context:[3,3,1,""]},"hutts_verification.image_processing.controllers":{extract_all:[3,5,1,""],extract_face:[3,5,1,""],extract_text:[3,5,1,""],face_extraction_response:[3,5,1,""]},"hutts_verification.image_processing.sample_extract":{FaceExtractor:[3,1,1,""],TextExtractor:[3,1,1,""]},"hutts_verification.image_processing.sample_extract.FaceExtractor":{extract:[3,3,1,""]},"hutts_verification.image_processing.sample_extract.TextExtractor":{extract:[3,3,1,""]},"hutts_verification.image_processing.simplification_manager":{SimplificationManager:[3,1,1,""]},"hutts_verification.image_processing.simplification_manager.SimplificationManager":{perspectiveTransformation:[3,3,1,""]},"hutts_verification.image_processing.text_cleaner":{TextCleaner:[3,1,1,""]},"hutts_verification.image_processing.text_cleaner.TextCleaner":{clean_up:[3,3,1,""]},"hutts_verification.utils":{hutts_logger:[4,0,0,"-"],image_handling:[4,0,0,"-"],pypath:[4,0,0,"-"]},"hutts_verification.utils.hutts_logger":{LOGGING_DEFAULT_LEVEL:[4,6,1,""],LOGGING_LOGGER_NAME:[4,6,1,""],LOGGING_LOG_DATE_FMT:[4,6,1,""],LOGGING_LOG_TO_CONSOLE:[4,6,1,""],LOGGING_LOG_TO_CONSOLE_COLOURS:[4,6,1,""],LOGGING_LOG_TO_CONSOLE_FMT:[4,6,1,""],LOGGING_LOG_TO_CONSOLE_SEC_COLOURS:[4,6,1,""],LOGGING_LOG_TO_FILE:[4,6,1,""],LOGGING_LOG_TO_FILE_BACKUP_COUNT:[4,6,1,""],LOGGING_LOG_TO_FILE_DEFAULT_DIR:[4,6,1,""],LOGGING_LOG_TO_FILE_ENCODING:[4,6,1,""],LOGGING_LOG_TO_FILE_FILENAME:[4,6,1,""],LOGGING_LOG_TO_FILE_FMT:[4,6,1,""],LOGGING_LOG_TO_FILE_MAX_BYTES:[4,6,1,""],disable_flask_logging:[4,5,1,""],get_console_handler:[4,5,1,""],get_file_handler:[4,5,1,""],prettify_json_message:[4,5,1,""],setup_logger:[4,5,1,""]},"hutts_verification.utils.image_handling":{grab_image:[4,5,1,""]},"hutts_verification.utils.pypath":{correct_path:[4,5,1,""]},"hutts_verification.verification":{controllers:[5,0,0,"-"],face_verify:[5,0,0,"-"],text_verify:[5,0,0,"-"]},"hutts_verification.verification.controllers":{manage_text_extractor:[5,5,1,""],manage_text_verification:[5,5,1,""],match_faces:[5,5,1,""],receive_details:[5,5,1,""],receive_faces:[5,5,1,""],verify_faces:[5,5,1,""],verify_id:[5,5,1,""],verify_info:[5,5,1,""]},"hutts_verification.verification.face_verify":{FaceVerify:[5,1,1,""]},"hutts_verification.verification.face_verify.FaceVerify":{verify:[5,3,1,""]},"hutts_verification.verification.text_verify":{TextVerify:[5,1,1,""]},"hutts_verification.verification.text_verify.TextVerify":{validate_id_number:[5,3,1,""],verify:[5,3,1,""]},hutts_verification:{id_contexts:[1,0,0,"-"],image_preprocessing:[2,0,0,"-"],image_processing:[3,0,0,"-"],utils:[4,0,0,"-"],verification:[5,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","method","Python method"],"4":["py","staticmethod","Python static method"],"5":["py","function","Python function"],"6":["py","data","Python data"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:method","4":"py:staticmethod","5":"py:function","6":"py:data"},terms:{"03d":4,"4aaqskzjrgabaqaaaqabaad":14,"4qtdrxh":14,"4qtdrxhpzgaa":14,"abstract":1,"boolean":[2,3,5],"byte":4,"case":4,"class":[1,2,3,5],"default":[4,5,7],"enum":1,"final":7,"float":5,"function":[2,3,4,5],"import":[4,13],"int":[2,3,5],"return":[1,2,3,4,5],"static":2,"true":[1,2,4,5,14],"try":7,"while":[4,5,13],For:[3,4],IDs:1,That:12,The:[1,2,3,4,5,7,8,9,11],There:4,These:[2,5],Using:[8,12],_deplor:3,_sa_id_book:3,_sa_id_book_old:3,_sa_id_card:3,_up_card:3,abc:1,abl:[2,3,5,13],abort:5,about:5,abov:5,accept:[1,5],accuraci:[2,5],activ:[2,13],adapt:2,adaptivethreshold:2,add:[2,8,11],added:2,adding:7,addit:5,adjust:[],affect:7,african:[1,3,7,8,11],after:[2,3,13],again:4,against:[5,14],align:[2,3],all:[1,2,3,5,13,14],allow:5,along:5,alphabet:1,alphanumer:1,alreadi:[7,13],also:[7,8,11,13,14],analyz:13,andrea:[],andreasnel:12,ani:[1,3,5,8,11,13],anoth:[7,8,11],anyth:13,api:[3,5,8,11],apidoc:[],app:4,app_inst:4,appli:[2,3,4,5],applic:[4,14],apply_barcode_blur:3,appropri:2,apt:13,arg:3,arrai:[2,3],asctim:4,assembl:2,assum:4,attempt:2,attribut:[],author:[],automat:[8,11],avail:13,avoid:4,backbon:7,background:7,backup:4,barcod:[1,3],barcode_data:1,barcode_manag:[0,6],barcodemanag:3,base64:[3,4,14],base:[1,2,3,5,8,11],basic:2,been:[2,3,13,14],befor:[2,4,5,12],being:[2,4,8,11],below:[4,5],benchmark:5,best:[5,7],better:8,between:5,bg_white:4,binari:2,birth:14,black:2,blackhat:2,blue:2,blur:[2,3],blur_fac:2,blur_kernel:2,blur_manag:[0,6],blur_typ:2,blurmanag:2,bold_cyan:4,bold_r:4,bold_whit:4,bold_yellow:4,book:[1,2,3,7,8,11],bool:[1,5],borntyp:4,both:[8,11,14],box:[2,3],build:[2,7,9],build_director:[0,6],builddirector:2,builder:2,built:[2,4,14],busier:7,calcul:5,calculatd:[],call:[1,2,4],can:[1,2,5,8,9,11,12,13,14],cannot:7,captur:[8,11],card:[1,2,3,7,8,11],chang:[2,4],channel:2,charact:[1,3,5],check:[1,2,4,5],choos:3,citizenship:14,classifi:2,clean:[3,8,11],clean_up:3,clone:13,close:5,cob:14,code:[3,9],collect:5,color:2,color_extraction_typ:2,color_manag:[0,6],colorlog:4,colormanag:2,colour:[2,4],com:[3,4,13],command:[12,13],compar:[1,5,8,11],comparison:3,compat:4,complet:13,compon:[],comput:[7,9,13],concret:1,confid:5,config:[],configur:[8,11],consid:[1,5],consol:4,constant:[],construct:2,construct_face_extract_pipelin:2,construct_text_extract_pipelin:2,contain:[1,2,3,5,7,12,14],containt:[],content:[6,8],context:[1,3],context_manag:[0,6],contextmanag:3,contextu:1,continu:2,contour:3,contour_area_threshold:[],control:[0,2,6],conveni:1,convert:[1,3],coordin:[2,3],copi:[2,3],core:[],correct:[4,5,7],correct_path:4,correctli:14,correspond:4,could:2,countri:14,country_of_birth:14,cours:14,creat:[2,4],creation:4,critic:[2,4],current:[3,4],custom:4,customiz:[],cv2:3,data:[2,3,5,8,11,14],date:[4,14],date_hyphen:1,date_of_birth:14,deal:14,debug:4,decid:5,deduc:2,defin:1,deleg:[1,4],demonstr:[1,3],depend:[7,13],deplor:3,descend:[],describ:[],descript:4,design:[2,8,11],desir:1,detail:[4,5],detect:[2,3,5],detector:2,determin:[1,2,3,5,7],dev0:13,dev:13,develop:[7,8,11],dict:[1,2,3,4,5],dictionari:[1,5],differ:[2,4,5,7,13],difficult:7,dilat:3,dilation_intens:3,dimens:2,directori:4,disabl:4,disable_flask_log:4,disk:[2,3,4],displai:[],dist:[4,13],distanc:5,dlib:[2,5],dob:14,docker:[8,9],document:[1,2,3,4,11,14],doe:[3,8],done:[1,2],down:1,download:7,driver:8,due:[2,7,8,11],dure:[1,2,3,4],dynam:2,each:[5,7],ean:3,eas:3,easier:7,easili:[8,11],edg:3,effect:2,effort:[5,7],either:[2,4,9],electron:[8,11],els:4,empti:3,encapsul:3,encod:4,end:1,ensur:5,enter:5,entered_detail:5,entir:2,enumer:1,environ:13,equalis:2,error:[1,4,13],especi:7,etc:2,euclidean:5,even:5,event:[3,4],everi:[],evid:[8,11],exactli:12,exampl:[1,4],execut:[2,13],exist:4,expect:5,experi:[8,11],explain:13,extend:3,extens:[],extent:3,extra:2,extract:[1,2,3,5,8,11],extract_al:3,extract_fac:[2,3],extract_text:3,extractal:[3,14],extractchannel:2,extracted_fac:14,extracted_text:5,extractfac:[3,14],extracttext:[3,14],extrem:7,face1:5,face2:5,face:[2,3,5,14],face_detector:2,face_extraction_respons:3,face_img:14,face_manag:[0,6],face_match:14,face_recognition_path:5,face_verifi:[0,6],facedetector:2,faceextractor:3,faceverifi:5,facial:[2,3,8,11,14],fact:2,fail:[],fals:[1,2,5,14],faq:8,featur:[2,7],fetch:4,field:[1,5],field_typ:1,fieldtyp:1,file:[1,3,4,5,7],filenam:4,filter:[1,3],find:[1,2],first:[3,4,5],flag:2,flask:[4,5],folder:4,follow:[5,12,13],font:7,form:5,format:4,formatt:4,found:[2,3,4],from:[1,2,3,4,5,8,9,11,14],frontal:2,frontal_fac:2,full:13,fulli:2,further:1,furthermor:3,futur:7,fuzzi:1,fuzzy_min_ratio:1,gaussian:2,gaussianblur:2,gender:14,gener:5,get:[12,13],get_barcode_info:3,get_console_handl:4,get_file_handl:4,get_frontal_face_detector:2,get_id_context:3,get_id_info:1,get_result:2,git:13,github:[4,13],give:[8,11],given:[1,4,5],global:4,grab:4,grab_imag:4,graphic:[8,11],greater:3,green:2,guarante:5,guess:7,handl:[2,3,4,5],handler:[4,5],hard:[],hardcod:[],hardwar:7,has:[2,3,4,5,7,14],hat:2,have:[7,13],help:4,helper:4,here:13,hermann:[],hierarchi:1,high:[1,2],higher:[1,5,7],highest:4,histequalis:2,histogram:2,hog:2,hour:13,hous:1,how:[3,5,14],howev:[5,7,8,11],html:2,http:[2,3,4,5,13,14],human:4,hutt:[9,11,12,13,14],hutts_logg:[0,6],hutts_util:[],hutts_verif:[8,13],id_context:[0,6],id_detail:3,id_img:14,id_numb:[1,5],id_str:1,id_typ:3,idcontext:[1,3],ideal:3,identif:[2,3,8,11,14],identifi:[1,2,7],identification_typ:2,identity_numb:14,idnumb:14,idphoto:14,ignor:1,ignore_field:1,imag:[2,3,4,5,8,14],image_channel:2,image_handl:[0,6],image_of_id:5,image_preprocess:[0,6],image_process:[0,6],img:3,impact:7,implement:[1,2],impli:14,in_str:3,includ:[2,5,7,8,11],increas:[2,7],inde:5,index:8,indic:[1,3,4,5],individu:5,info:4,inform:[1,2,3,5,8,11,14],inherit:1,initialis:4,input:3,insid:7,instal:[4,7,8,14],install_depend:13,instead:[],instruct:8,integ:[2,3,5],intend:1,intens:3,interfac:[8,11],interfer:4,intermedi:[],internet:[],intro:[],introduct:[],invalid:2,invers:2,is_match:14,is_pass:14,issu:[4,7],item:2,iter:[],itf:3,its:[1,4,7],ivar:[],jan:[],java:13,javathehutt:13,jhutt:12,jpeg:14,jpg:[3,14],json:[4,5,14],json_messag:4,just:1,justin:[],kernel:2,kernel_s:2,kind:7,know:1,known:4,label:5,labl:5,lamin:7,larg:8,larger:7,later:2,latest:12,lead:7,length:[2,5],less:2,level:[1,2,4],levelnam:4,libboost:13,librari:[5,7],libzbar0:13,libzbar:13,licens:8,like:[2,3,5,12],likelihood:1,line:1,line_typ:1,linear:2,lineno:4,linetyp:1,link:13,list:[1,2,3,5],local:7,localhost:[3,5,14],locat:3,log:[2,4],log_color:4,log_dir:4,logger:[4,5],logging_default_level:4,logging_log_date_fmt:4,logging_log_to_consol:4,logging_log_to_console_colour:4,logging_log_to_console_fmt:4,logging_log_to_console_sec_colour:4,logging_log_to_fil:4,logging_log_to_file_backup_count:4,logging_log_to_file_default_dir:4,logging_log_to_file_encod:4,logging_log_to_file_filenam:4,logging_log_to_file_fmt:4,logging_log_to_file_max_byt:4,logging_logger_nam:4,logic:[1,3,4,5],longer:8,look:[1,7],loss:5,lower:[4,7],lowest:4,made:14,mai:[5,7,13],main:[8,11],mainli:1,maintain:3,major:2,make:[2,5,7,9,12,14],manag:[2,3,4,5],manage_text_extractor:5,manage_text_verif:5,manger:3,manipul:2,manner:[8,11],manual:[8,9,11],market:[8,11],marno:[],match:[1,5,8,11],match_context:1,match_fac:5,max_multi_lin:1,maxdepth:[],maximum:[1,4,7],mean:[4,5,7],mechan:7,median:2,medianblur:2,messag:[4,5],message_log_color:4,method:[1,2,9,14],might:2,mime:14,min_age_delta:1,min_match:5,minimum:[1,5],minut:13,mix:1,mode:4,modifi:2,modul:[6,8],moment:[],more:[2,3,4,7],morpholog:2,most:4,msec:4,multi:1,multi_lin:1,multi_line_end:1,multipl:[1,5],must:[1,2,3,5],name:[1,4,14],nameerror:2,nation:14,necessari:[1,2,4],need:[2,5,8,11],nel:[],nell:[],net:2,network:7,newlin:1,next:1,nicolai:[],niekerk:[],nois:[2,3],non:3,none:[1,2,3,4],normal:2,note:[1,13],noth:3,now:[4,12],number:[1,4,5,7,14],numer:[1,5],numeric_onli:1,numpi:[2,3],obj:[2,3,4,5],object:[1,2,3,5],ocr:[1,3,13],offici:[8,11],old:3,one:[1,4],onli:[1,5,7,8,11,14],onto:1,opencv:[2,4,7,13],oper:[1,4,5],optim:7,optimis:2,option:1,order:[5,7,8,11,12,13,14],origin:[2,3],other:[2,5,8],otherwis:[1,5],otso:[],otsu:2,otsuthreshold:2,our:[7,12],out:3,output:[1,3],own:7,packag:[6,8],page:8,param:2,paramet:[1,2,3,4,5,7],parent:1,part:2,particular:1,pass:[2,3,5],passport:8,path:[4,5],pattern:2,pdf417:[],penalti:2,percentag:[5,8,11],perform:[2,8,11],person:[5,8,11,14],perspect:[2,3],perspectivetransform:3,phase:2,pictur:[5,7],pip3:13,pipelin:[0,6],pipeline_build:[0,6],pipelinebuild:2,plan:7,pleas:[12,13],pluggabl:[8,11],poor:7,port:12,posit:[2,5],possibl:[8,11],post:[1,14],post_process_min_fuzzy_ratio:1,potenti:[3,7],pre:[1,2],preced:1,predefin:2,prefer:[2,3,5,12],prepar:5,preprocess:[],present:[2,3,7],pretoria:[1,3,7,8,11],prettifi:4,prettify_json_messag:4,previou:[8,11],primari:[8,11],problem:[],proceed:12,process:[1,2,3,8],process_face_extract:2,process_text_extract:2,produc:3,profil:5,project:13,provid:[2,3,5,8,11,14],publish:13,pull:12,purpos:[1,8,11],pyb:13,pybuild:13,pypath:[0,6],python3:13,python:[4,8,11,13],pyzbar:13,qualiti:7,rais:[1,2,3,4,5],rather:2,ratio:1,readabl:4,reappli:[2,3],reason:7,receiv:[2,3,5,14],receive_detail:5,receive_fac:5,recommend:5,rect_kernel_s:2,red:[2,4],reduc:[1,2,3,8,11],refer:4,regard:4,region:[2,3],rel:1,relat:2,relev:[1,3,5,14],remov:[1,2,3],remove_fac:2,repositori:13,repres:[1,2,4,5],represent:5,request:[3,5,12,14],requir:[2,3,4,8,13],reset:4,resid:[2,3,4],respons:[1,2,3,4,5,14],result:[2,3,5],retriev:1,right:3,rotat:4,run:[1,4,7,12,13,14],sa_id:[0,6],sa_id_book:[0,6],sa_id_book_old:[0,6],sa_id_card:[0,6],said:[1,3],saidbook:[1,3],saidbookold:[1,3],saidcard:[1,3],same:5,sampl:[3,5,14],sample_extract:[0,6],scan:[3,7],scandit:3,score:5,script:13,search:[2,8],second:5,secondari:4,section:[12,14],see:[2,4],select:2,self:5,send:14,sent:5,serv:[1,3],server:[4,7,8,11,12],servic:[3,5],set:[1,2,5,8,11,14],set_blur_manag:2,set_color_manag:2,set_face_detector:2,set_threshold_manag:2,setup:[4,13],setup_logg:4,sever:2,sex:14,shape_predictor_path:[2,5],shell:13,should:[1,2,3,4,5,13,14],shown:4,simpl:[2,8,11],simpli:5,simplif:3,simplifi:3,simplification_manag:[0,6],simplificationmanag:3,sinc:[],site:4,size:[2,7],slow:7,smaller:[],solut:5,solv:4,some:[1,8],someon:[],sort:[],sourc:[1,2,3,4,5,8,9],south:[1,3,7,8,11],span:1,specif:[1,2],specifi:[1,2,4,5],speed:7,src:2,stack:1,staff:3,stage:[7,8,11],standard:5,start:[4,12],statement:13,statu:14,stephan:[],still:5,str:[1,2,3,4,5],stream:[4,5],string:[1,3,4,5,14],strip:3,student:[3,7,8,11],submodul:[0,6],subpackag:6,success:13,successfulli:[],sudo:13,suppli:1,support:3,sure:12,surnam:[1,14],system:[5,7,8,9,11,12],take:[3,8,11,13],target:[8,11,13],techniqu:2,templat:[2,8,11],template_match:[0,6],templatematch:2,tend:7,tesseract:13,test:13,text:[2,3,4,5,14],text_clean:[0,6],text_extract_result:[3,14],text_match:14,text_match_percentag:[],text_onli:1,text_verif:5,text_verifi:[0,6],textclean:3,textextractor:3,textual:[8,11,14],textverifi:5,than:[2,3,4,8],thei:7,them:5,therefor:7,thi:[1,2,3,4,5,7,8,11,13,14],threshold:[1,2,5],threshold_manag:2,thresholding_manag:[0,6],thresholding_typ:2,thresholdingmanag:2,thresholdmanag:2,through:[3,7],thu:[2,3],time:[2,8,11],titl:1,titled_adjac:1,titled_newlin:1,to_uppercas:1,toctre:[],todo:[],tonder:[],top:[2,7],tophat:2,total:5,total_match:14,transform:3,transmiss:3,treat:1,tupl:2,tutori:13,two:[1,5,8,11],txt:13,type:[1,2,3,5,8,11,14],typeerror:[1,2,3,5],undesir:[1,3],univers:[1,3,7,8,11],unless:[1,4],unnecessari:3,unrecognis:3,untitled_adjac:1,untitled_newlin:1,unwant:3,up_student_card:[0,6],upc:3,upload:[4,7],uppercas:1,upstudentcard:[1,3],url:[3,4,5,14],usag:4,use:[2,4,5,7,8,9,11,12,14],use_io:3,used:[1,2,3,4,5,7],useio:2,user:[2,5,8,9,11,13,14],using:2,utf8:4,utf:3,util:[0,6],valid:[1,2,5],valid_id_length:1,valid_length:5,validate_id_numb:[1,5],valu:[1,2,3,5],valueerror:[2,4,5],van:[],variou:[3,4],vector:5,verbos:5,verbose_verifi:14,veri:7,verif:[0,6,9,11,12,13],verifi:[5,14],verification_threshold:14,verify_fac:5,verify_id:5,verify_info:5,verifyfac:5,verifyid:[5,14],verifyinfo:[],version:13,via:[8,9],view:3,virtual:13,wai:[],warn:4,warp:[],watermark:7,web:[8,11],well:[1,3,8,11,14],what:[1,4,5,7],when:[1,2,4,14],where:[2,4],whether:[1,2,3,4,5,13],which:[1,2,3,4,5,7,13,14],white:2,whitespac:3,why:8,wild:5,wish:[],within:2,without:[2,5,8,11,13],work:[8,11],would:3,wrap:[2,3,4],write:[2,3],written:3,www:3,year_delta:1,you:[2,7,12],your:[7,12,13],zbar:13},titles:["hutts_verification package","hutts_verification.id_contexts package","hutts_verification.image_preprocessing package","hutts_verification.image_processing package","hutts_verification.utils package","hutts_verification.verification package","hutts_verification","Frequently Asked Questions","Welcome to Hutts Verification\u2019s documentation!","Requirements and Installation Instructions","Using the Interface","Introduction","Installing via Docker","Installing from Source Code","Using the Server"],titleterms:{Using:[10,14],african:[],all:[],andrea:[],api:[],ask:7,author:[],barcode_manag:3,better:7,blur_manag:2,build_director:2,can:7,card:[],code:13,color_manag:2,contain:[],content:[0,1,2,3,4,5],context:[],context_manag:3,control:[3,5],data:7,directori:[],docker:[7,12],document:[7,8],doe:7,driver:7,extract:[7,14],face_manag:2,face_verifi:5,file:[],frequent:7,from:[7,13],handl:[],help:[],hermann:[],hutt:[7,8],hutts_logg:4,hutts_util:[],hutts_verif:[0,1,2,3,4,5,6],id_context:1,imag:7,image_handl:4,image_preprocess:2,image_process:3,indic:8,instal:[9,12,13],instruct:9,interfac:10,introduct:[8,11],issu:[],jan:[],justin:[],larg:7,lib:[],licens:7,logic:[],longer:7,marno:[],modul:[0,1,2,3,4,5],nel:[],nell:[],nicolai:[],niekerk:[],other:7,packag:[0,1,2,3,4,5],passport:7,path:[],pipelin:2,pipeline_build:2,process:7,pypath:4,python:[],question:7,relev:[],request:[],requir:9,sa_id:1,sa_id_book:1,sa_id_book_old:1,sa_id_card:1,sample_extract:3,server:14,servic:[],simplification_manag:3,solv:[],some:7,sourc:13,south:[],stephan:[],submodul:[1,2,3,4,5],subpackag:0,tabl:8,take:7,template_match:2,text_clean:3,text_verifi:5,than:7,thi:[],thresholding_manag:2,tonder:[],type:7,up_student_card:1,util:4,valid:[],van:[],verif:[5,7,8,14],via:12,welcom:8,why:7,work:7}})