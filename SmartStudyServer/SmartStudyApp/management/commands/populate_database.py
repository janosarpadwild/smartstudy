from django.core.management.base import BaseCommand
from SmartStudyApp import models
from django.db import transaction
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **options):
        with transaction.atomic():      
            #admins
            print('Create', models.User.__name__)    
            try:
                admin, _ = models.User.objects.get_or_create(
                    email= 'admin@admin.com',
                    name= 'admin',
                    password= make_password('admin'),
                    is_superuser = True,
                    is_staff = True
                )
            except Exception as e:
                print('Could not create', models.User.__name__, e)
            #schools -------------------------------------------
            print('Create', models.School.__name__)
            try:
                school1, _ = models.School.objects.get_or_create(
                    name='Parkside High School'
                )
            except Exception as e:
                print('Could not create', models.School.__name__, e)
            #secretaries -------------------------------------------
            print('Create', models.User.__name__)
            try:
                #school 1 -------------------------------------------
                secretary1, _ = models.User.objects.get_or_create(
                    email= 'susan.parkside@example.com',
                    name= 'Susan Johnson',
                    password= make_password('mJq2|Y;?0pKC0Ng'),
                    school_id= school1,
                    role= 'SECRETARY'
                )
            except Exception as e:
                print('Could not create', models.User.__name__, e)
            #teachers -------------------------------------------
            print('Create', models.User.__name__)
            try:
                #school 1 -------------------------------------------
                physic_teacher1, _ = models.User.objects.get_or_create(
                    email= 'alice.parkside@example.com',
                    name= 'Alice Thompson',
                    password= make_password('Oy7bpC(M]q!{A3)'),
                    school_id= school1,
                    role= 'TEACHER',
                    secretary_id=secretary1
                )
                physic_teacher2, _ = models.User.objects.get_or_create(
                    email= 'john.parkside@example.com',
                    name= 'John Roberts',
                    password= make_password('?+&(KK$I0fQ)m1k'),
                    school_id= school1,
                    role= 'TEACHER',
                    secretary_id=secretary1
                )
                not_physic_teacher, _ = models.User.objects.get_or_create(
                    email= 'sarah.parkside@example.com',
                    name= 'Sarah Williams',
                    password= make_password('=<LX"e=XFii:8-n'),
                    school_id= school1,
                    role= 'TEACHER',
                    secretary_id=secretary1
                )

                transmitted_teacher, _ = models.User.objects.get_or_create(
                    email= 'lisa.parkside@example.com',
                    name= 'Lisa Garcia',
                    password= make_password('Sp6t.[;)Z]s(fCg'),
                    school_id= school1,
                    role= 'TEACHER',
                )
                archived_teacher, _ = models.User.objects.get_or_create(
                    email= 'ashley.parkside@example.com',
                    name= 'Ashley Lee',
                    password= make_password('E2Ex/V#-ha=pw(C'),
                    school_id= school1,
                    archived=True,
                    role= 'TEACHER',
                )

            except Exception as e:
                print('Could not create', models.User.__name__, e)
            #classes -------------------------------------------
            try:
                #school 1 -------------------------------------------
                class1, _ = models.Class.objects.get_or_create(
                    name= '8. a',
                    school_id= school1,
                    secretary_id= secretary1
                )
                transmitted_class, _ = models.Class.objects.get_or_create(
                    name= '9. b',
                    school_id= school1
                )

            except Exception as e:
                print('Could not create', models.Class.__name__, e)
            #students -------------------------------------------
            print('Create', models.User.__name__)
            try:
                #school 1 -------------------------------------------
                student1_class1, _ = models.User.objects.get_or_create(
                    email= 'anbqo6@inf.elte.hu',
                    name= 'Wild János',
                    password= make_password('J478E$a6|d.adh/'),
                    school_id= school1,
                    secretary_id= secretary1,
                    class_id= class1,
                    role= 'STUDENT'
                )
                student2_class1, _ = models.User.objects.get_or_create(
                    email= 'student2@example.com',
                    name= 'Student Two',
                    password= make_password('J478E$a6|d.adh/'),
                    school_id= school1,
                    secretary_id= secretary1,
                    class_id= class1,
                    role= 'STUDENT'
                )
                student3_class1, _ = models.User.objects.get_or_create(
                    email= 'student3@example.com',
                    name= 'Student Three',
                    password= make_password('J478E$a6|d.adh/'),
                    school_id= school1,
                    secretary_id= secretary1,
                    class_id= class1,
                    role= 'STUDENT'
                )
                student1_transmitted_class, _ = models.User.objects.get_or_create(
                    email= 'student4@example.com',
                    name= 'Transmitted Student1',
                    password= make_password('J478E$a6|d.adh/'),
                    school_id= school1,
                    class_id= transmitted_class,
                    role= 'STUDENT'
                )
                student2_transmitted_class, _ = models.User.objects.get_or_create(
                    email= 'student5@example.com',
                    name= 'Transmitted Student2',
                    password= make_password('J478E$a6|d.adh/'),
                    school_id= school1,
                    class_id= transmitted_class,
                    role= 'STUDENT'
                )
                student3_transmitted_class, _ = models.User.objects.get_or_create(
                    email= 'student6@example.com',
                    name= 'Transmitted Student3',
                    password= make_password('J478E$a6|d.adh/'),
                    school_id= school1,
                    class_id= transmitted_class,
                    role= 'STUDENT'
                )
                transmitted_student, _ = models.User.objects.get_or_create(
                    email= 'student7@example.com',
                    name= 'Transmitted Student4',
                    password= make_password('J478E$a6|d.adh/'),
                    school_id= school1,
                    role= 'STUDENT'
                )
                archived_student, _ = models.User.objects.get_or_create(
                    email= 'student8@example.com',
                    name= 'Archived Student',
                    password= make_password('J478E$a6|d.adh/'),
                    school_id= school1,
                    archived=True,
                    role= 'STUDENT'
                )
            except Exception as e:
                print('Could not create', models.User.__name__, e)
            #subjects -------------------------------------------
            print('Create', models.Subject.__name__)
            try:
                subject1, _ = models.Subject.objects.get_or_create(
                    name='fizika'
                )
                subject2, _ = models.Subject.objects.get_or_create(
                    name='kémia'
                )
                subject3, _ = models.Subject.objects.get_or_create(
                    name='matematika'
                )
            except Exception as e:
                print('Could not create', models.Subject.__name__, e)
            #teachersubject -------------------------------------------
            print('Create', models.TeacherSubject.__name__)
            try:
                #school 1 -------------------------------------------
                subject1_teacher1, _ = models.TeacherSubject.objects.get_or_create(
                    subject_name = subject1,
                    teacher_id = physic_teacher1,
                )
                subject2_teacher1_school1, _ = models.TeacherSubject.objects.get_or_create(
                    subject_name = subject2,
                    teacher_id = physic_teacher1,
                )
                subject1_teacher2_school1, _ = models.TeacherSubject.objects.get_or_create(
                    subject_name = subject1,
                    teacher_id = physic_teacher2,
                )
                subject2_teacher2_school1, _ = models.TeacherSubject.objects.get_or_create(
                    subject_name = subject3,
                    teacher_id = physic_teacher2,
                )
                subject1_teacher3_school1, _ = models.TeacherSubject.objects.get_or_create(
                    subject_name = subject2,
                    teacher_id = not_physic_teacher,
                )
                subject3_teacher3_school1, _ = models.TeacherSubject.objects.get_or_create(
                    subject_name = subject3,
                    teacher_id = not_physic_teacher,
                )
                subject1_teacher4_school1, _ = models.TeacherSubject.objects.get_or_create(
                    subject_name = subject1,
                    teacher_id = transmitted_teacher,
                )
                subject2_teacher4_school1, _ = models.TeacherSubject.objects.get_or_create(
                    subject_name = subject2,
                    teacher_id = archived_teacher,
                )
            except Exception as e:
                print('Could not create', models.TeacherSubject.__name__, e)
            #topics -------------------------------------------
            print('Create', models.Topic.__name__)
            try:
                topic1, _ = models.Topic.objects.get_or_create(
                    name= 'Pontok, pontrendszerek',
                    number= 1,
                    description= 'Pontszerű testre ható erők eredője, fonálra függesztett test, kifeszített fonálra függesztett test',
                    subject_name= subject1,
                )
                topic2, _ = models.Topic.objects.get_or_create(
                    name= 'Emelők',
                    number= 2,
                    description= 'Egykarú- kétkarú- nem szimmetrikus kétkarú emelő egyensúlya, homogén tömegeloszlású rúd egyensúlya',
                    subject_name= subject1,
                )
                topic3, _ = models.Topic.objects.get_or_create(
                    name= 'Csigák',
                    number= 3,
                    description= 'Teher mozgatása állócsiga és mozgócsiga segítségével, munka és teljesítmény számolása állócsiga esetében',
                    subject_name= subject1,
                )
                topic4, _ = models.Topic.objects.get_or_create(
                    name= 'Lejtők, létrák',
                    number= 4,
                    description= 'Lejtőn lecsűszó test gyorulása, lejtőn lévő test egyensúlya, egy- és kétágú létra lábaiban ható erők és egyensúlyi állapot számolása',
                    subject_name= subject1,
                )
            except Exception as e:
                print('Could not create', models.Topic.__name__, e)
            #subtopics ------------------------------------------- 
            print('Create', models.SubTopic.__name__)
            try:
                subtopic1_topic1, _ = models.SubTopic.objects.get_or_create(
                    topic_id= topic1,
                    name= 'Ponszerű testre ható erők eredőjének kiszámítása',
                    number= 1,
                    parameters= [{"objects":[], "texts":{}, "variables":{
                                    'a':{'min':2,'max':20},
                                    'b':{'min':2,'max':20}
                                }},
                                 {"objects":[], "texts":{}, "variables":{
                                     'a':{'min':1,'max':10},
                                     'b':{'min':1,'max':10},
                                     'c':{'min':1,'max':10},
                                     'd':{'min':1,'max':10}
                                 }},
                                 {"objects":[], "texts":{}, "variables":{
                                     'm1':{'min':2,'max':10},
                                     'm2':{'min':2,'max':10},
                                     'l':{'min':2,'max':5}
                                 }},
                                 {"objects":[], "texts":{}, "variables":{
                                     'a':{'min':0.5,'max':2},
                                     'm':{'min':0.2,'max':1}
                                 }}],
                    tutorial_description= [{'question':'Pontszerű testre két erő hat: észak fele {a}N nyugat fele {b}N. Mekkora lesz az eredő erő?', 'method':'A Pitagorasz-tétel alapján az erők eredője két erő négyzetösszegének gyöke.', 'answer':'négyzetgyök(a^2+b^2)'},
                                           {'question': 'Pontszerű testre négy erő hat: észak fele {a}N, nyugat felé {b}N, dél felé {c}N, kelet felé {d}N. Mekkora lesz az erők eredője?', 'method': 'A Pitagorasz-tétel alapján az erők eredője az egy egyenesbe eső erők vektori eredőjének négyzetösszegének a gyökét vesszük.', 'answer': 'négyzetgyök((a-c)^2+(b-d)^2)'},
                                           {'question': 'Hol van az egymástól {l}m távolságra lévő {m1}kg, és {m2}kg tömegű pontszerű testekből álló rendszer súlypontja az {m1}kg tömegponthoz képest?', 'method': 'A tömegközéppont távolsága a pontszerű testektől fordítottan arányos a tömegekkel. A tömeg és a távolság szorzata állandó, így m1*x = m2*(l-x).', 'answer': 'm1*x = m2*l-m2*x\nm1*x+m2*x = m2*l\nx*(m1+m2) = m2*l\nm2*l/(m1+m2)'},
                                           {'question': '{a}m oldalú egyenlő szárú derékszögű háromszög három csúcsába ugyanakkora {m}kg tömegű pontszerű testeket teszünk. A derékszögű csúcstól milyen távol lesz a három pontból álló rendszer tömegközéppontja?', 'method': 'Az átfogó végpontjaiba helyezett testek tömegközéppontjának helye az átfogó felezőpontja, tehát a probléma veisszavezethető a következőre: az átfogó felezőpontjában van {2*m}tömegű test, a derékszögű csúcsban {m}tömegű test, melyek távolsága az átfogó fele. A tömegközéppont távolsága a pontszerű testektől fordítottan arányos a tömegekkel, ezért a tömegközéppont helye a derékszögű csúcstól az átfogó felének a kétharmada.', 'answer': '2/3*a*négyzetgyök(2)/2\na*négyzetgyök(2)/3'}]
                )
                subtopic2_topic1, _ = models.SubTopic.objects.get_or_create(
                    topic_id= topic1,
                    name= 'Fonálra függesztett test',
                    number= 2,
                    parameters= [{"objects":[], "texts":{}, "variables":{
                        'm':{'min':0.5,'max':5},
                        'g':{'min':10,'max':10},
                        'a':{'min':20,'max':60}
                    }}],
                    tutorial_description= [{'question': 'Fonálra függesztett {m*g}N súlyú testet vízszintes irányban oldalt húzunk. Mekkora erővel húzza a fonál a testet, ha az a függőlegessel {a}fokos szöget zár be? (g=10m/s^2)', 'method': 'A testet pontszerű testnek tekinthetjük, a pontszerű test egyensúlyának feltétele az, hogy a testre ható erők eredője nulla legyen. A testre három erő hat, a (test tömege)*(gravitációs gyorsulás) lefele, a húzóerő oldalra, és a kötélerő ferdén. A három erő eredője akkor nulla, ha teljesül az m*g/cos(a)', 'answer': 'f = m*g /cos(a)\nm*g /cos(a)'}]
                )
                subtopic3_topic1, _ = models.SubTopic.objects.get_or_create(
                    topic_id= topic1,
                    name= 'Két oldalt azonos magasságban kifeszített fonálra függeszetett test',
                    number= 3,
                    parameters= [{"objects":[], "texts":{}, "variables":{
                        'm':{'min':1,'max':5},
                        'g':{'min':10,'max':10},
                        'x':{'min':10,'max':60}
                    }}],
                    tutorial_description= [{'question': 'Két ház között egyforma magasságban kifeszített huzalon {m}kg tömegű lámpa függ az oszlopoktól egyenlő távolságra. Mekkora erő feszíti a huzalt, ha az a vízszintessel {x}fokos szöget zár be?', 'method': 'A kétirányú kötélerők egyenlőek, a függőleges összetevőik összege egyenlő a lámpa súlyával, tehát egy kötél függőleges erőjének nagysága a test súlyának a fele. Mivel az erővektorok derékszögű háromszöget határoznak meg, a kötélerő szögfüggvénnyel számolható a kötél vízszintessel bezárt szögének ismeretében.', 'answer': 'sin(a) = 0.5*m*g/K\nK = 0.5*m*g/sin(a)\n0.5*m*g/sin(a)'}]
                )
                subtopic1_topic2, _ = models.SubTopic.objects.get_or_create(
                    topic_id= topic2,
                    name= 'Egy és kétkarú emelő egyensúlyának létrehozása különböző erők, erőkarok esetében',
                    number= 1,
                    parameters= [{"objects":[], "texts":{}, "variables":{
                                    'a':{'min':0.5,'max':2},
                                    'b':{'min':0.1,'max':10},
                                    'x':{'min':1,'max':10}
                                }},
                                {"objects":[], "texts":{}, "variables":{
                                'a':{'min':0.5,'max':5},
                                'x':{'min':1,'max':10},
                                'l':{'min':5,'max':20}
                                }}],
                    tutorial_description= [{'question': 'Középen alátámasztott kétoldalú emelő egyik oldalán a tengelytől {a}m távolságra {x}N erő hat lefelé. Mekkora erő tudná az emelőt egyensúlyban tartani a másik oldalon, a tengelytől {b}m távolságban?', 'method': 'A testek egyensúlyának feltétele, hogy a forgatónyomatékok eredője nulla legyen, azaz az egyik oldalon ha az erőt megszorzom az erőkarral, meg kell egyezzen a másik oldalon ható erő szorozva másik oldalhoz tartozó erőkarral.', 'answer': 'a*x = b*y\na*x/b'},
                                           {'question': 'Egyoldalú emelő esetén a forgástengelytől {a}m távolságban {x}N erő hat lefelé. Mekkora függőleges irányú erővel tudjuk az {l}m hosszúságú emelőt egyensúlyban tartani az emelő végpontjában?', 'method': 'A testek egyensúlyának feltétele, hogy a forgatónyomatékok eredője nulla legyen, azaz a lefelé ható erő forgatónyomatéka meg kell egyezzen a végpontban felfelé ható erő forgatónyomatékával. Ha az ismert erőt megszorzom a forgástengelytől mért távolságával, a szorzat meg kell egyezzen az ismeretlen erő szorozva az ő forgástengelytől mért távolságával.', 'answer': 'a*x = l*y\na*x/l'}]
                )
                subtopic2_topic2, _ = models.SubTopic.objects.get_or_create(
                    topic_id= topic2,
                    name= 'Homogén tömegeloszlású rúd egyensúlyának feltétele különböző terhelések esetén',
                    number= 2,
                    parameters= [{"objects":[], "texts":{}, "variables":{
                                    'x':{'min':10,'max':100},
                                    'l':{'min':5,'max':10},
                                    'k':{'min':1,'max':5},
                                    'm':{'min':5,'max':50}
                                }},
                                {"objects":[], "texts":{}, "variables":{
                                    'x':{'min':10,'max':100},
                                    'l':{'min':5,'max':10},
                                    'k':{'min':1,'max':5},
                                    'm':{'min':5,'max':50}
                                }}],
                    tutorial_description= [{'question': 'Egy {x}N súlyú, {l}m hosszú homogén tömegeloszlású gerenda egyik végén, és a másik végétől {k}m távolságra van alátámasztva. A gerenda szabad végén {m}N súlyú test lóg. Mekkora erő hat a rúd végén lévő alátámasztási pontra?', 'method': 'Vegyük a forgástengelyt a végétől {k}m távolságra lévő alátámasztásoz, és írjuk fel az erre a pontra vonatkozó forgatónyomatékokat. Ezeknek a forgatónyomatékoknak a rúd két oldalán egyenlőnek kell lenni.', 'answer': 'k*m = (l/2-k)*x+(l-k)*F\n(k*m-(l/2-k)*x)/(l-k)'},
                                           {'question': 'Egy {x}N súlyú, {l}m hosszú homogén tömegeloszlású gerenda egyik végén, és a másik végétől {k}m távolságra van alátámasztva. A gerenda szabad végén {m}N súlyú test lóg. Mekkora erő hat a rúd végétől {k}m távolságra lévő alátámasztási pontra?', 'method': 'Vegyük a forgástengelyt a rúd végén lévő alátámasztási ponthoz, és írjuk fel az erre a pontra vonatkozó forgatónyomatékokat. Ezeknek a forgatónyomatékoknak a rúd két oldalán egyenlőnek kell lenni.', 'answer': 'm*l+x*l/2=(l-k)*F\n(m*l+x*l/2)/(l-k)'}]
                )
                subtopic3_topic2, _ = models.SubTopic.objects.get_or_create(
                    topic_id= topic2,
                    name= 'Csuklóval falhoz erősített homogén tömegeloszlású rúd egyensúlyának kiszámítása',
                    number= 3,
                    parameters= [{"objects":[], "texts":{}, "variables":{
                                    'x':{'min':10,'max':50},
                                    'l':{'min':2,'max':5},
                                    'y':{'min':10,'max':50}
                                }},
                                {"objects":[], "texts":{}, "variables":{
                                    'x':{'min':10,'max':50},
                                    'l':{'min':2,'max':5},
                                    'y':{'min':10,'max':50}
                                }}],
                    tutorial_description= [{'question': 'Egy {l}m hosszú {x}N súlyú homogén tömegeloszlású rudat csuklóval erősítünk egy falhoz. A rúd végére {y}N súlyú testet akasztunk. Mekkora erővel tudjuk a rudat a végénél megfogva vízszintes helyzetben tartani?', 'method': 'A rúdra két forgatónyomaték hat lefele, középen a rúd súlyából származó, a rúd végénél a ráakasztott test súlyából származó. Ezek összegével egyenlő annak az erőnek a forgatónyomatéka amellyel vízszintes helyzetben tarthatjuk.', 'answer': 'x*l/2+y*l = l*f\nf = (x*l/2+y*l)/l\nx/2+y'},
                                           {'question': 'Egy {l}m hosszú {x}N súlyú homogén tömegeloszlású rudat csuklóval erősítünk egy falhoz. A rúd fal felőli negyedelőpontjához {y}N súlyú testet akasztunk. Mekkora erővel tudjuk a rudat a végénél megfogva vízszintes helyzetben tartani?', 'method': 'A rúdra két forgatónyomaték hat lefele, középen a rúd súlyából származó, a rúd negyedénél a ráakasztott test súlyából származó. Ezek összegével egyenlő annak az erőnek a forgatónyomatéka amellyel vízszintes helyzetben tarthatjuk.', 'answer': 'l/4*y+l/2*x=l*f\ny/4+x/2'}]
                )
                subtopic4_topic2, _ = models.SubTopic.objects.get_or_create(
                    topic_id= topic2,
                    name= 'Nem szimmetrikus kétoldalú emelő egyensúlyának kiszámítása',
                    number= 4,
                    parameters= [{"objects":[], "texts":{}, "variables":{
                                    'x':{'min':10,'max':50}
                                }},
                                {"objects":[], "texts":{}, "variables":{
                                    'x':{'min':10,'max':50}
                                }}],
                    tutorial_description= [{'question': 'Egyharmadánál alátámasztott kétoldalú emelő a tengelyhez közelebbi végpontjában {x}N erő hat lefelé. Mekkora erő tudná az emelőt egyensúlyban tartani a másik oldalon?', 'method': 'A testek egyensúlyának feltétele, hogy a forgatónyomatékok eredője nulla legyen, azaz az egyik oldalon ha az erőt megszorzom az erőkarral, meg kell egyezzen a másik oldalon ható erő szorozva másik oldalhoz tartozó erőkarral.', 'answer': 'x/2'},
                                           {'question': 'Kétötöd részénél alátámasztott kétoldalú emelő a tengelyhez közelebbi végpontjában {x}N erő hat lefelé. Mekkora erő tudná az emelőt egyensúlyban tartani a másik oldalon?', 'method': 'A testek egyensúlyának feltétele, hogy a forgatónyomatékok eredője nulla legyen, azaz az egyik oldalon ha az erőt megszorzom az erőkarral, meg kell egyezzen a másik oldalon ható erő szorozva másik oldalhoz tartozó erőkarral.', 'answer': 'x*2=y*3\nx*2/3'}]
                )
                subtopic1_topic3, _ = models.SubTopic.objects.get_or_create(
                    topic_id= topic3,
                    name= 'Teher mozgatása álló- és mozgócsiga segítségével',
                    number= 2,
                    parameters= [{"objects":[
                                    ['#1_ellipse',{'x':'size_x/2', 'y':'30', 'width':'30', 'height':'30'}],
                                    ['x_rect',{'x':'size_x/2-eval(objects[1][1]["width"])/2', 'y':'size_y/2', 'width':'30', 'height':'30'}, {'start':'eval(objects[1][1]["y"])', 'stop':'eval(objects[1][1]["y"])-eval(objects[2][1]["length"])/2*scale', 'type':1}],      
                                    ['#2_line',{'length':'(eval(objects[1][1]["y"])-eval(objects[2][1]["y"]))/scale', 'x':'size_x/2', 'y':'30+eval(objects[0][1]["height"])/2', 'angle':90, 'arrow':'none'}, {'start':'eval(objects[2][1]["length"])', 'stop':'eval(objects[2][1]["length"])/2', 'type':0}],
                                    ['#3_line',{'length':'(eval(objects[1][1]["y"])-eval(objects[0][1]["y"])-eval(objects[0][1]["height"])/2)/scale', 'x':'eval(objects[0][1]["x"])+eval(objects[0][1]["width"])', 'y':'eval(objects[0][1]["y"])+eval(objects[0][1]["height"])/2', 'angle':90, 'arrow':'end'}, {'start':'eval(objects[2][1]["length"])', 'stop':'eval(objects[2][1]["length"])*1.5', 'type':0}]
                                ],
                                    "texts":{'x_rect':'N', '#3_line':'?'},
                                    "variables":{'x':{'min':200,'max':500}}
                                    },
                                {"objects":[['#0_ellipse',{'x':'size_x/2-eval(objects[0][1]["width"])', 'y':'30', 'width':'30', 'height':'30'}],
                                            ['x_rect',{'x':'size_x/2', 'y':'size_y-30-eval(objects[1][1]["height"])', 'width':'30', 'height':'30'}, {'start':'eval(objects[1][1]["y"])', 'stop':'eval(objects[1][1]["y"])-eval(objects[4][1]["length"])/2*scale', 'type':1}],
                                            ['#2_ellipse',{'x':'size_x/2', 'y':'size_y/2-eval(objects[2][1]["height"])', 'width':'30', 'height':'30'}, {'start':'eval(objects[2][1]["y"])', 'stop':'eval(objects[2][1]["y"])-eval(objects[4][1]["length"])/2*scale', 'type':1}],
                                            ['#3_line',{'length':'size_y/2-eval(objects[3][1]["y"])', 'x':'eval(objects[0][1]["x"])', 'y':'eval(objects[0][1]["y"])+eval(objects[0][1]["height"])/2', 'angle':90, 'arrow':'end'},  {'start':'eval(objects[3][1]["length"])', 'stop':'eval(objects[3][1]["length"])*scale+eval(objects[4][1]["length"])/2*scale', 'type':0}],
                                            ['#4_line',{'length':'size_y/2-60-eval(objects[0][1]["height"])/2', 'x':'size_x/2', 'y':'eval(objects[0][1]["y"])+eval(objects[0][1]["height"])/2', 'angle':90, 'arrow':'none'}, {'start':'eval(objects[4][1]["length"])', 'stop':'eval(objects[4][1]["length"])/2', 'type':0}],
                                            ['#5_line',{'length':'size_y/2-60', 'x':'size_x/2+eval(objects[2][1]["width"])', 'y':'30', 'angle':90, 'arrow':'none'}, {'start':'eval(objects[5][1]["length"])', 'stop':'eval(objects[5][1]["length"])-eval(objects[4][1]["length"])/2*scale', 'type':0}],
                                            ['#6_line',{'length':'eval(objects[1][1]["y"])-eval(objects[6][1]["y"])', 'x':'eval(objects[1][1]["x"])+eval(objects[1][1]["width"])/2', 'y':'eval(objects[2][1]["y"])+eval(objects[2][1]["height"])/2', 'angle':90, 'arrow':'none'}, {'start':'eval(objects[6][1]["y"])', 'stop':'eval(objects[6][1]["y"])-eval(objects[4][1]["length"])/2', 'type':1}]],
                                             "texts":{'x_rect':'N', '#4_line':'?'},
                                             "variables":{'x':{'min':200,'max':500}}},
                                ],
                    tutorial_description= [{'question': 'Állócsigán {x}N súlyú vödör van. Mekkora erővel tudjuk felhúzni a vödröt?', 'method': 'Az egyenletes mozgás feltétele, hogy a testre ható erők eredője nulla legyen, tehát a húzóerő meg kell egyezzen a vödör súlyával.', 'answer': 'f = x\nx'},
                                           {'question': 'Egy {x}N súlyú testet egy álló- és egy mozgócsiga segítségével szeretnénk felhúzni. Mekkora erővel tudjuk felhúzni?', 'method': 'Ha a rendszerben egy mozgócsiga van, akkor a húzóerő fele lesz a test súlyának.', 'answer': 'f = x/2\nx/2'}])
                subtopic2_topic3, _ = models.SubTopic.objects.get_or_create(
                    topic_id= topic3,
                    name= 'Munka és teljesítmény számolása állócsiga esetében',
                    number= 1,
                    parameters= [{"objects":[], "texts":{}, "variables":{
                                    'x':{'min':10,'max':30},
                                    'g':{'min':10,'max':10},
                                    'h':{'min':10,'max':30}
                                }},
                                {"objects":[], "texts":{}, "variables":{
                                    'x':{'min':10,'max':30},
                                    'g':{'min':10,'max':10},
                                    'h':{'min':10,'max':30},
                                    't':{'min':30,'max':60}
                                }}],
                    tutorial_description= [{'question': 'Állócsiga segítségével {x}l vizet szeretnénk felhúzni egy {h}m mély kútból egyenletes sebességgel. Mekkora lesz a végzett munka (1l víz = 1kg, g=10m/s*2)?', 'method': 'A munka az erő és elmozdulás szorzata. Ebben az esetben az erő a víz súlya, az elmozdulás a kút mélysége.', 'answer': 'w = x*g*h\nx*g*h'},
                                           {'question': 'Állócsiga segítségével {x}l vizet szeretnénk felhúzni egy {h}m mély kútból {t}s idő alatt egyenletes sebességgel. Mekkora a teljesítményünk (1l víz = 1kg, g=10m/s*2)?', 'method': 'A teljesítményt a végzett munka és az idő hányadosával számoljuk. A munka az erő és elmozdulás szorzata. Ebben az esetben az erő a víz súlya, az elmozdulás a kút mélysége. Ezeknek szorzatát kell elosztani a munkavégzéshez szükséges idővel.', 'answer': 'p = x*g*h/t\nx*g*h/t'}]
                )
                subtopic1_topic4, _ = models.SubTopic.objects.get_or_create(
                    topic_id= topic4,
                    name= 'Lejtőn lecsúszó test gyorsulásának és lejtőn lévő test egyensúlyának számítása',
                    number= 1,
                    parameters= [{"objects":[], "texts":{}, "variables":{
                                    'm':{'min':2,'max':5},
                                    'a':{'min':30,'max':60}
                                }},
                                {"objects":[], "texts":{}, "variables":{
                                    'm':{'min':1,'max':10},
                                    'a':{'min':30,'max':60}
                                }}],
                    tutorial_description= [{'question': '{a}hajlásszögű lejtőn súrlódás nélkül csúszik le egy {m}kg tömegő test. Mekkora lesz a test gyorsulása?', 'method': 'A testre ható gravitációs erőt felbonthatjuk egy lejtővel párhuzamos és merőleges összetevőre. A merőleges összetevőt a lejtőnek a testre ható ereje kiegyenlíti. Tehát a testre ható erők eredője a lejtővel párhuzamos összetevő lesz, melyet szögfüggvénnyel kiszámolhatunk (sin(a)).', 'answer': 'a = F/m = m*g*sin(a)/m = g*sin(a)\ng*sin(a)\nm/s^2'},
                                           {'question': '{a}hajlásszögű lejtőre egy {m}kg tömegű testet helyezünk. A testre nyújthatatlan fonalat kötünk, melyre a lejtő tetején rögzített csigán átvetve egy {n}kg tömegű testet helyezünk. Mekkora legyen ennek a felfüggesztett testnek a tömege, hogy a lejtőn lévő test egyensúlyban maradjon?', 'method': 'A testre ható gravitációs erőt felbonthatjuk egy lejtővel párhuzamos és merőleges összetevőre. A merőleges összetevőt a lejtőnek a testre ható ereje kiegyenlíti. Tehát a testre ható erők eredője a lejtővel párhuzamos összetevő lesz, ezzel kell egyenlő legyen a felfüggesztett testre ható gravitációs erő.', 'answer': 'n=m*sin(a)\nm*sin(a)'}]
                )
                subtopic2_topic4, _ = models.SubTopic.objects.get_or_create(
                    topic_id= topic4,
                    name= 'Egy- és kétágú létrában ható erők, és egyensúlyi állapot kiszámítása',
                    number= 2,
                    parameters= [{"objects":[], "texts":{}, "variables":{
                                    'a':{'min':20,'max':40},
                                    'b':{'min':400,'max':800}
                                }},
                                {"objects":[], "texts":{}, "variables":{
                                    'a':{'min':20,'max':40},
                                    'b':{'min':400,'max':800}
                                }},
                                {"objects":[], "texts":{}, "variables":{
                                    'a':{'min':20,'max':40},
                                    'b':{'min':400,'max':800}
                                }},
                                {"objects":[], "texts":{}, "variables":{
                                    'm':{'min':2,'max':10},
                                    'l':{'min':2,'max':5},
                                    'a':{'min':20,'max':40}
                                }}],
                    tutorial_description= [{'question': 'Kétágú létra szárai {a}fokos szöget zárnak be egymással. A létra tetején egy {b}N súlyú ember áll. Mekkora erővel nyomja a létra egyik szára a talajt?', 'method': 'A létra a talajt függőleges irányban nyomja, tehát az ember súlyának a felével.', 'answer': 'f = b/2\nb/2'},
                                           {'question': 'Kétágú létra szárai {a}fokos szöget zárnak be egymással. A létra tetején egy {b}N súlyú ember áll. Mekkorák a létra száraiban ható erők?', 'method': 'Ezt a szögfüggvény segítségével kiszámolhatjuk. A létra szára a függőlegessel azaz az ember súlya erejével {a}/2 szöget zár be.', 'answer': 'cos(a/2) = 0.5*b/F\nF = 0.5*b/cos(a/2)\n0.5*b/cos(a/2)'},
                                           {'question': 'Kétágú létra szárai {a}fokos szöget zárnak be egymással. A létra tetején egy {b}N súlyú ember áll. Mekkor erő igyekszik vízszintes irányban csúsztatni a létra szárait?', 'method': 'Az ember súlyának fele a létra egyik szárára nehezedik, a másik fele a létra másik szárára. A létrában ható erő vízszintes összetevője lesz a keresett erő. Ezt a szögfüggvény segítségével kiszámolhatjuk. A létra szára a függőlegessel azaz az ember súlya erejével {a}/2 szöget zár be.', 'answer': 'F/0.5*b = tg(a/2)\nF = 0.5*b*tg(a/2)\n0.5*b*tg(a/2)'},
                                           {'question': 'Egyágú, {m}kg tömegű, {l}m hosszúságú létrát támasztunk {a}fokos szögben a falhoz. Mekkora erővel nyomja a falat (g=10m/s^2)?', 'method': 'A forgatónyomatékot a létra talajjal érintkező végpontjába írjuk fel. Erre a pontra nézve a létrára ható gravitációs erőnek és a fal erejének van forgató hatása. E két erő forgatónyomatékának kell egyenlőnek lennie.', 'answer': 'k1 = l*sin(a)/2\nk2 = l*cos(a)\nm*g*l*sin(a)/2 = F*l*cos(a)\nF = m*g/2*tg(a)\nm*g/2*tg(a)'}]
                )
            except Exception as e:
                print('Could not create', models.SubTopic.__name__, e)
            #tasks -------------------------------------------
            print('Create', models.Task.__name__)
            try:
                task1_subtopic1_topic1, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic1_topic1,
                    number = 1,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'a':{'min':2,'max':20},
                        'b':{'min':2,'max':20}
                    }},
                    question = 'Pontszerű testre két erő hat: észak fele {a}N nyugat fele {b}N. Mekkora lesz az eredő erő?',
                    answer = 'math.sqrt({a}^2+{b}^2)',
                    unit = 'N'
                )
                task2_subtopic1_topic1, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic1_topic1,
                    number = 2,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'a':{'min':1,'max':10},
                        'b':{'min':1,'max':10},
                        'c':{'min':1,'max':10},
                        'd':{'min':1,'max':10}
                    }},
                    question = 'Pontszerű testre négy erő hat: észak fele {a}N, nyugat felé {b}N, dél felé {c}N, kelet felé {d}N. Mekkora lesz az erők eredője?',
                    answer = 'math.sqrt(({a}-{c})^2+({b}-{d})^2)',
                    unit = 'N'
                )
                task3_subtopic1_topic1, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic1_topic1,
                    number = 3,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'm1':{'min':2,'max':10},
                        'm2':{'min':2,'max':10},
                        'l':{'min':2,'max':5}
                    }},
                    question = 'Hol van az egymástól {l}m távolságra lévő {m1}kg, és {m2}kg tömegű pontszerű testekből álló rendszer súlypontja az {m1}kg tömegponthoz képest?',
                    answer = '{m2}*{l}/({m1}+{m2})',
                    unit = 'm'
                )
                task4_subtopic1_topic1, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic1_topic1,
                    number = 4,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'a':{'min':0.5,'max':2},
                        'm':{'min':0.2,'max':1}
                    }},
                    question = '{a}m oldalú egyenlő szárú derékszögű háromszög három csúcsába ugyanakkora {m}kg tömegű pontszerű testeket teszünk. A derékszögű csúcstól milyen távol lesz a három pontból álló rendszer tömegközéppontja?',
                    answer = '{a}*math.sqrt(2)/3',
                    unit = 'm'
                )
                task1_subtopic2_topic1, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic2_topic1,
                    number = 1,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'm':{'min':0.5,'max':5},
                        'g':{'min':10,'max':10},
                        'a':{'min':20,'max':60}}},
                    question = 'Fonálra függesztett {m*g}N súlyú testet vízszintes irányban oldalt húzunk. Mekkora erővel húzza a fonál a testet, ha az a függőlegessel {a}fokos szöget zár be? (g=10m/s^2)',
                    answer = '{m}*{g} /math.cos(math.radians({a}))',
                    unit = 'N'
                )
                task1_subtopic3_topic1, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic3_topic1,
                    number = 1,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'm':{'min':1,'max':5},
                        'g':{'min':10,'max':10},
                        'x':{'min':10,'max':60}}},
                    question = 'Két ház között egyforma magasságban kifeszített huzalon {m}kg tömegű lámpa függ az oszlopoktól egyenlő távolságra. Mekkora erő feszíti a huzalt, ha az a vízszintessel {x}fokos szöget zár be?',
                    answer = '0.5*{m}*{g}/math.sin(math.radians({x}))',
                    unit = 'N'
                )
                task1_subtopic1_topic2, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic1_topic2,
                    number = 1,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'a':{'min':0.5,'max':2},
                        'b':{'min':0.1,'max':10},
                        'x':{'min':1,'max':10}}},
                    question = 'Középen alátámasztott kétoldalú emelő egyik oldalán a tengelytől {a}m távolságra {x}N erő hat lefelé. Mekkora erő tudná az emelőt egyensúlyban tartani a másik oldalon, a tengelytől {b}m távolságban?',
                    answer = '{a}*{x}/{b}',
                    unit = 'N'
                )
                task2_subtopic1_topic2, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic1_topic2,
                    number = 2,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'a':{'min':0.5,'max':5},
                        'x':{'min':1,'max':10},
                        'l':{'min':5,'max':20}}},
                    question = 'Egyoldalú emelő esetén a forgástengelytől {a}m távolságban {x}N erő hat lefelé. Mekkora függőleges irányú erővel tudjuk az {l}m hosszúságú emelőt egyensúlyban tartani az emelő végpontjában?',
                    answer = '{a}*{x}/{l}',
                    unit = 'N'
                )
                task1_subtopic2_topic2, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic2_topic2,
                    number = 1,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'x':{'min':10,'max':100},
                        'l':{'min':5,'max':10},
                        'k':{'min':1,'max':5},
                        'm':{'min':5,'max':50}}},
                    question = 'Egy {x}N súlyú, {l}m hosszú homogén tömegeloszlású gerenda egyik végén, és a másik végétől {k}m távolságra van alátámasztva. A gerenda szabad végén {m}N súlyú test lóg. Mekkora erő hat a rúd végén lévő alátámasztási pontra?',
                    answer = '({k}*{m}-({l}/2-{k})*{x})/({l}-{k})',
                    unit = 'N'
                )
                task2_subtopic2_topic2, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic2_topic2,
                    number = 2,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'x':{'min':10,'max':100},
                        'l':{'min':5,'max':10},
                        'k':{'min':1,'max':5},
                        'm':{'min':5,'max':50}}},
                    question = 'Egy {x}N súlyú, {l}m hosszú homogén tömegeloszlású gerenda egyik végén, és a másik végétől {k}m távolságra van alátámasztva. A gerenda szabad végén {m}N súlyú test lóg. Mekkora erő hat a rúd végétől {k}m távolságra lévő alátámasztási pontra?',
                    answer = '({m}*{l}+{x}*{l}/2)/({l}-{k})',
                    unit = 'N'
                )
                task1_subtopic3_topic2, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic3_topic2,
                    number = 1,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'x':{'min':10,'max':50},
                        'l':{'min':2,'max':5},
                        'y':{'min':10,'max':50}}},
                    question = 'Egy {l}m hosszú {x}N súlyú homogén tömegeloszlású rudat csuklóval erősítünk egy falhoz. A rúd végére {y}N súlyú testet akasztunk. Mekkora erővel tudjuk a rudat a végénél megfogva vízszintes helyzetben tartani?',
                    answer = '{x}/2+{y}',
                    unit = 'N'
                )
                task2_subtopic3_topic2, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic3_topic2,
                    number = 2,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'x':{'min':10,'max':50},
                        'l':{'min':2,'max':5},
                        'y':{'min':10,'max':50}}},
                    question = 'Egy {l}m hosszú {x}N súlyú homogén tömegeloszlású rudat csuklóval erősítünk egy falhoz. A rúd fal felőli negyedelőpontjához {y}N súlyú testet akasztunk. Mekkora erővel tudjuk a rudat a végénél megfogva vízszintes helyzetben tartani?',
                    answer = '{y}/4+{x}/2',
                    unit = 'N'
                )
                task1_subtopic4_topic2, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic4_topic2,
                    number = 1,
                    parameters = {"objects":[], "texts":{}, "variables":{'x':{'min':10,'max':50}}},
                    question = 'Egyharmadánál alátámasztott kétoldalú emelő a tengelyhez közelebbi végpontjában {x}N erő hat lefelé. Mekkora erő tudná az emelőt egyensúlyban tartani a másik oldalon?',
                    answer = '{x}/2',
                    unit = 'N'
                )
                task2_subtopic4_topic2, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic4_topic2,
                    number = 2,
                    parameters = {"objects":[], "texts":{}, "variables":{'x':{'min':10,'max':50}}},
                    question = 'Kétötöd részénél alátámasztott kétoldalú emelő a tengelyhez közelebbi végpontjában {x}N erő hat lefelé. Mekkora erő tudná az emelőt egyensúlyban tartani a másik oldalon?',
                    answer = '{x}*2/3',
                    unit = 'N'
                )
                task1_subtopic1_topic3, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic1_topic3,
                    number = 1,
                    parameters = {"objects":[
                                    ['#1_ellipse',{'x':'size_x/2', 'y':'30', 'width':'30', 'height':'30'}],
                                    ['x_rect',{'x':'size_x/2-eval(objects[1][1]["width"])/2', 'y':'size_y/2', 'width':'30', 'height':'30'}, {'start':'eval(objects[1][1]["y"])', 'stop':'eval(objects[1][1]["y"])-eval(objects[2][1]["length"])/2*scale', 'type':1}],      
                                    ['#2_line',{'length':'(eval(objects[1][1]["y"])-eval(objects[2][1]["y"]))/scale', 'x':'size_x/2', 'y':'30+eval(objects[0][1]["height"])/2', 'angle':90, 'arrow':'none'}, {'start':'eval(objects[2][1]["length"])', 'stop':'eval(objects[2][1]["length"])/2', 'type':0}],
                                    ['#3_line',{'length':'(eval(objects[1][1]["y"])-eval(objects[0][1]["y"])-eval(objects[0][1]["height"])/2)/scale', 'x':'eval(objects[0][1]["x"])+eval(objects[0][1]["width"])', 'y':'eval(objects[0][1]["y"])+eval(objects[0][1]["height"])/2', 'angle':90, 'arrow':'end'}, {'start':'eval(objects[2][1]["length"])', 'stop':'eval(objects[2][1]["length"])*1.5', 'type':0}]
                                ],
                                    "texts":{'x_rect':'N', '#3_line':'?'},
                                    "variables":{'x':{'min':200,'max':500}}},
                    question = 'Állócsigán {x}N súlyú vödör van. Mekkora erővel tudjuk felhúzni a vödröt?',
                    answer = '{x}',
                    unit = 'N'
                )
                task2_subtopic1_topic3, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic1_topic3,
                    number = 2,
                    parameters = {"objects":[['#0_ellipse',{'x':'size_x/2-eval(objects[0][1]["width"])', 'y':'30', 'width':'30', 'height':'30'}],
                                            ['x_rect',{'x':'size_x/2', 'y':'size_y-30-eval(objects[1][1]["height"])', 'width':'30', 'height':'30'}, {'start':'eval(objects[1][1]["y"])', 'stop':'eval(objects[1][1]["y"])-eval(objects[4][1]["length"])/2*scale', 'type':1}],
                                            ['#2_ellipse',{'x':'size_x/2', 'y':'size_y/2-eval(objects[2][1]["height"])', 'width':'30', 'height':'30'}, {'start':'eval(objects[2][1]["y"])', 'stop':'eval(objects[2][1]["y"])-eval(objects[4][1]["length"])/2*scale', 'type':1}],
                                            ['#3_line',{'length':'size_y/2-eval(objects[3][1]["y"])', 'x':'eval(objects[0][1]["x"])', 'y':'eval(objects[0][1]["y"])+eval(objects[0][1]["height"])/2', 'angle':90, 'arrow':'end'},  {'start':'eval(objects[3][1]["length"])', 'stop':'eval(objects[3][1]["length"])*scale+eval(objects[4][1]["length"])/2*scale', 'type':0}],
                                            ['#4_line',{'length':'size_y/2-60-eval(objects[0][1]["height"])/2', 'x':'size_x/2', 'y':'eval(objects[0][1]["y"])+eval(objects[0][1]["height"])/2', 'angle':90, 'arrow':'none'}, {'start':'eval(objects[4][1]["length"])', 'stop':'eval(objects[4][1]["length"])/2', 'type':0}],
                                            ['#5_line',{'length':'size_y/2-60', 'x':'size_x/2+eval(objects[2][1]["width"])', 'y':'30', 'angle':90, 'arrow':'none'}, {'start':'eval(objects[5][1]["length"])', 'stop':'eval(objects[5][1]["length"])-eval(objects[4][1]["length"])/2*scale', 'type':0}],
                                            ['#6_line',{'length':'eval(objects[1][1]["y"])-eval(objects[6][1]["y"])', 'x':'eval(objects[1][1]["x"])+eval(objects[1][1]["width"])/2', 'y':'eval(objects[2][1]["y"])+eval(objects[2][1]["height"])/2', 'angle':90, 'arrow':'none'}, {'start':'eval(objects[6][1]["y"])', 'stop':'eval(objects[6][1]["y"])-eval(objects[4][1]["length"])/2', 'type':1}]],
                                             "texts":{'x_rect':'N', '#4_line':'?'},
                                             "variables":{'x':{'min':200,'max':500}}},
                    question = 'Egy {x}N súlyú testet egy álló- és egy mozgócsiga segítségével szeretnénk felhúzni. Mekkora erővel tudjuk felhúzni?',
                    answer = '{x}/2',
                    unit = 'N'
                )
                
                task1_subtopic2_topic3, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic2_topic3,
                    number = 1,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'x':{'min':10,'max':30},
                        'g':{'min':10,'max':10},
                        'h':{'min':10,'max':30}}},
                    question = 'Állócsiga segítségével {x}l vizet szeretnénk felhúzni egy {h}m mély kútból egyenletes sebességgel. Mekkora lesz a végzett munka (1l víz = 1kg, g=10m/s*2)?',
                    answer = '{x}*{g}*{h}',
                    unit = 'J'
                )
                task2_subtopic2_topic3, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic2_topic3,
                    number = 2,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'x':{'min':10,'max':30},
                        'g':{'min':10,'max':10},
                        'h':{'min':10,'max':30},
                        't':{'min':30,'max':60}}},
                    question = 'Állócsiga segítségével {x}l vizet szeretnénk felhúzni egy {h}m mély kútból {t}s idő alatt egyenletes sebességgel. Mekkora a teljesítményünk (1l víz = 1kg, g=10m/s*2)?',
                    answer = '{x}*{g}*{h}/{t}',
                    unit = 'W'
                )
                task1_subtopic1_topic4, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic1_topic4,
                    number = 1,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'g':{'min':10,'max':10},
                        'm':{'min':2,'max':5},
                        'a':{'min':30,'max':60}}},
                    question = '{a}hajlásszögű lejtőn súrlódás nélkül csúszik le egy {m}kg tömegő test. Mekkora lesz a test gyorsulása?',
                    answer = '{g}*math.sin(math.radians({a}))',
                    unit = 'm/s^2'
                )
                task2_subtopic1_topic4, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic1_topic4,
                    number = 2,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'm':{'min':1,'max':10},
                        'a':{'min':30,'max':60},
                        'n':{'min':10, 'max':20}}},
                    question = '{a}hajlásszögű lejtőre egy {m}kg tömegű testet helyezünk. A testre nyújthatatlan fonalat kötünk, melyre a lejtő tetején rögzített csigán átvetve egy {n}kg tömegű testet helyezünk. Mekkora legyen ennek a felfüggesztett testnek a tömege, hogy a lejtőn lévő test egyensúlyban maradjon?',
                    answer = '{m}*math.sin(math.radians({a}))',
                    unit = 'kg'
                )
                task1_subtopic2_topic4, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic2_topic4,
                    number = 1,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'a':{'min':20,'max':40},
                        'b':{'min':400,'max':800}}},
                    question = 'Kétágú létra szárai {a}fokos szöget zárnak be egymással. A létra tetején egy {b}N súlyú ember áll. Mekkora erővel nyomja a létra egyik szára a talajt?',
                    answer = '{b}/2',
                    unit = 'N'
                )
                task2_subtopic2_topic4, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic2_topic4,
                    number = 2,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'a':{'min':20,'max':40},
                        'b':{'min':400,'max':800}}},
                    question = 'Kétágú létra szárai {a}fokos szöget zárnak be egymással. A létra tetején egy {b}N súlyú ember áll. Mekkorák a létra száraiban ható erők?',
                    answer = '0.5*{b}/math.cos(math.radians({a}/2))',
                    unit = 'N'
                )
                task3_subtopic2_topic4, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic2_topic4,
                    number = 3,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'a':{'min':20,'max':40},
                        'b':{'min':400,'max':800}}},
                    question = 'Kétágú létra szárai {a}fokos szöget zárnak be egymással. A létra tetején egy {b}N súlyú ember áll. Mekkor erő igyekszik vízszintes irányban csúsztatni a létra szárait?',
                    answer = '0.5*{b}*math.tan(math.radians({a}/2))',
                    unit = 'N'
                )
                task4_subtopic2_topic4, _ = models.Task.objects.get_or_create(
                    subtopic_id = subtopic2_topic4,
                    number = 4,
                    parameters = {"objects":[], "texts":{}, "variables":{
                        'g':{'min':10,'max':10},
                        'm':{'min':2,'max':10},
                        'l':{'min':2,'max':5},
                        'a':{'min':20,'max':40}}},
                    question = 'Egyágú, {m}kg tömegű, {l}m hosszúságú létrát támasztunk {a}fokos szögben a falhoz. Mekkora erővel nyomja a falat (g=10m/s^2)?',
                    answer = '{m}*{g}/2*math.tan(math.radians({a}))',
                    unit = 'N'                    
                )
            except Exception as e:
                print('Could not create', models.Task.__name__, e)
            #course & coursetopic -------------------------------------------
            print('Create', models.Course.__name__, models.CourseTopic.__name__)
            try:
                #school 1 -------------------------------------------
                course1 = models.Course.objects.create(
                    name="fizika",
                    class_id=class1,
                    subject_name=subject1
                )

            except Exception as e:
                print('Could not create', models.Course.__name__, models.CourseTopic.__name__, e)
            #teachercourse -------------------------------------------
            print('Create', models.TeacherCourse.__name__)
            try:
                #school 1 -------------------------------------------
                teachercourse1, _ = models.TeacherCourse.objects.get_or_create(
                    teacher_id = physic_teacher1,
                    course_id = course1
                )
                teachercourse2, _ = models.TeacherCourse.objects.get_or_create(
                    teacher_id = physic_teacher2,
                    course_id = course1
                )

            except Exception as e:
                print('Could not create', models.TeacherCourse.__name__, e)
            #completedtopic, testresult, completedsubtopic -------------------------------------------
            print('Create', models.CompletedTopic.__name__, models.CompletedSubTopic.__name__, models.TestResult.__name__)
            try:
                with transaction.atomic():
                    # Update or create CourseTopic
                    coursetopic1, _ = models.CourseTopic.objects.get_or_create(
                        course_id=course1,
                        topic_id=topic1,
                        test_task_number = 10,
                        test_required_percentage = 60,
                        available = False
                    )
                    coursetopic2, _ = models.CourseTopic.objects.get_or_create(
                        course_id=course1,
                        topic_id=topic2,
                        test_task_number = 15,
                        test_required_percentage = 75,
                        available = False
                    )
                    coursetopic3, _ = models.CourseTopic.objects.get_or_create(
                        course_id=course1,
                        topic_id=topic3,
                        test_task_number = 2,
                        test_required_percentage = 50,
                        available = True
                    )
                    coursetopic4, _ = models.CourseTopic.objects.get_or_create(
                        course_id=course1,
                        topic_id=topic4,
                        test_task_number = 8,
                        test_required_percentage = 50,
                        available = True
                    )

                    # Update or create CompletedTopic
                    completed_topic13, _ = models.CompletedTopic.objects.get_or_create(
                        student_id=student1_class1,
                        course_id=course1,
                        topic_id=topic3,
                    )
                    completed_topic14, _ = models.CompletedTopic.objects.get_or_create(
                        student_id=student1_class1,
                        course_id=course1,
                        topic_id=topic4,
                        completed_topic = True
                    )
                    completed_topic23, _ = models.CompletedTopic.objects.get_or_create(
                        student_id=student2_class1,
                        course_id=course1,
                        topic_id=topic3,
                    )
                    completed_topic24, _ = models.CompletedTopic.objects.get_or_create(
                        student_id=student2_class1,
                        course_id=course1,
                        topic_id=topic4,
                        completed_topic = True
                    )
                    completed_topic33, _ = models.CompletedTopic.objects.get_or_create(
                        student_id=student3_class1,
                        course_id=course1,
                        topic_id=topic3,
                        completed_topic = True
                    )
                    completed_topic34, _ = models.CompletedTopic.objects.get_or_create(
                        student_id=student3_class1,
                        course_id=course1,
                        topic_id=topic4,
                    )

                    # Update or create TestResult
                    test_result113, _ = models.TestResult.objects.get_or_create(
                        student_id=student1_class1,
                        course_id=course1,
                        topic_id=topic3,
                        last_correct_answers=0,
                        best_correct_answers=0
                    )
                    test_result114, _ = models.TestResult.objects.get_or_create(
                        student_id=student1_class1,
                        course_id=course1,
                        topic_id=topic4,
                        last_correct_answers=6,
                        best_correct_answers=6
                    )
                    test_result213, _ = models.TestResult.objects.get_or_create(
                        student_id=student2_class1,
                        course_id=course1,
                        topic_id=topic3,
                        last_correct_answers=0,
                        best_correct_answers=0
                    )
                    test_result214, _ = models.TestResult.objects.get_or_create(
                        student_id=student2_class1,
                        course_id=course1,
                        topic_id=topic4,
                        last_correct_answers=5,
                        best_correct_answers=7
                    )
                    test_result313, _ = models.TestResult.objects.get_or_create(
                        student_id=student3_class1,
                        course_id=course1,
                        topic_id=topic3,
                        last_correct_answers=1,
                        best_correct_answers=1
                    )
                    test_result314, _ = models.TestResult.objects.get_or_create(
                        student_id=student3_class1,
                        course_id=course1,
                        topic_id=topic4,
                        last_correct_answers=0,
                        best_correct_answers=0
                    )

                    # Iterate over subtopics
                    completed_subtopic131, _ = models.CompletedSubTopic.objects.get_or_create(
                        student_id=student1_class1,
                        course_id=course1,
                        subtopic_id=subtopic1_topic3,
                        number=2,
                        completed_tutorial= False,
                        completed_subtopic= False
                    )
                    completed_subtopic132, _ = models.CompletedSubTopic.objects.get_or_create(
                        student_id=student1_class1,
                        course_id=course1,
                        subtopic_id=subtopic2_topic3,
                        number=1,
                        completed_tutorial= True,
                        completed_subtopic= True
                    )
                    completed_subtopic141, _ = models.CompletedSubTopic.objects.get_or_create(
                        student_id=student1_class1,
                        course_id=course1,
                        subtopic_id=subtopic1_topic4,
                        number=1,
                        completed_tutorial= True,
                        completed_subtopic= True
                    )
                    completed_subtopic142, _ = models.CompletedSubTopic.objects.get_or_create(
                        student_id=student1_class1,
                        course_id=course1,
                        subtopic_id=subtopic2_topic4,
                        number=2,
                        completed_tutorial= True,
                        completed_subtopic= True
                    )
                    completed_subtopic231, _ = models.CompletedSubTopic.objects.get_or_create(
                        student_id=student2_class1,
                        course_id=course1,
                        subtopic_id=subtopic1_topic3,
                        number=2,
                        completed_tutorial= False,
                        completed_subtopic= False
                    )
                    completed_subtopic232, _ = models.CompletedSubTopic.objects.get_or_create(
                        student_id=student2_class1,
                        course_id=course1,
                        subtopic_id=subtopic2_topic3,
                        number=1,
                        completed_tutorial= False,
                        completed_subtopic= False
                    )
                    completed_subtopic241, _ = models.CompletedSubTopic.objects.get_or_create(
                        student_id=student2_class1,
                        course_id=course1,
                        subtopic_id=subtopic1_topic4,
                        number=1,
                        completed_tutorial= True,
                        completed_subtopic= True
                    )
                    completed_subtopic242, _ = models.CompletedSubTopic.objects.get_or_create(
                        student_id=student2_class1,
                        course_id=course1,
                        subtopic_id=subtopic2_topic4,
                        number=2,
                        completed_tutorial= True,
                        completed_subtopic= True
                    )
                    completed_subtopic331, _ = models.CompletedSubTopic.objects.get_or_create(
                        student_id=student3_class1,
                        course_id=course1,
                        subtopic_id=subtopic1_topic3,
                        number=2,
                        completed_tutorial= True,
                        completed_subtopic= True
                    )
                    completed_subtopic332, _ = models.CompletedSubTopic.objects.get_or_create(
                        student_id=student3_class1,
                        course_id=course1,
                        subtopic_id=subtopic2_topic3,
                        number=1,
                        completed_tutorial= True,
                        completed_subtopic= True
                    )
                    completed_subtopic341, _ = models.CompletedSubTopic.objects.get_or_create(
                        student_id=student3_class1,
                        course_id=course1,
                        subtopic_id=subtopic1_topic4,
                        number=1,
                        completed_tutorial= True,
                        completed_subtopic= True
                    )
                    completed_subtopic342, _ = models.CompletedSubTopic.objects.get_or_create(
                        student_id=student3_class1,
                        course_id=course1,
                        subtopic_id=subtopic2_topic4,
                        number=2,
                        completed_tutorial= True,
                        completed_subtopic= False
                    )

            except Exception as e:
                print('Could not create', models.CompletedTopic.__name__, models.CompletedSubTopic.__name__, models.TestResult.__name__, e)
