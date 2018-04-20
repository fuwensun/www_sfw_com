from webapp.extensions import celery
import smtplib
import datetime
from email.mime.text import MIMEText
from flask import render_template
from webapp.extensions import debug,celery
from webapp.models import Reminder, Post, db, Comment

# celery worker -A celery_runner --loglevel=info    #异步task必须启动worker进程
# celery -A celery_runner beat                      #定时器task必须启动beat进程

def debug_tasks(str):
    debug(" <==!tasks print!==> " + str)

@celery.task()
def log(msg):
    debug_tasks("log()")
    return msg

@celery.task()
def multiply(x, y):
    debug_tasks("log()")
    return x*y

@celery.task()
def m(x, y):
    debug_tasks("m()")
    return x*y

@celery.task()
def xx_new_comment(self, pk):
    debug_tasks("xx_new_comment()")
    s  = "remind task()" + "  self = " + str(self) + "  pk = " + str(pk)
    new_comment = Comment()
    new_comment.name = s
    new_comment.text = s
    new_comment.post_id = 1
    new_comment.date = datetime.datetime.now()
    # db.session.add(new_comment)
    # db.session.commit()
    return "remind task()" + "  self = " + str(self) + "  pk = " + str(pk)

@celery.task(
    bind=True,               #task对象 绑定第一个参数self
    #ignore_result=True,     #如果启用remind.get（） 和 ready（）会阻塞
    default_retry_delay=30,  # default_retry_delay=1000,
    max_retries=5
)
def remind(self, pk):
    debug_tasks("remind()")
    s  = str(self) + "  pk = " + str(pk)
    new_comment = Comment()
    new_comment.name = s
    new_comment.text = s
    new_comment.post_id = 1
    new_comment.date = datetime.datetime.now()
    return s

    reminder = Reminder.query.get(pk)
    msg = MIMEText(reminder.text)

    msg['Subject'] = "Your reminder"
    msg['From'] = ""
    msg['To'] = reminder.email

    try:
        smtp_server = smtplib.SMTP('localhost')
        smtp_server.starttls()
        # smtp_server.login(user, password)
        smtp_server.sendmail("", [reminder.email], msg.as_string())
        smtp_server.close()

        # debug("debug--remind task()" + "  self = " + str(self) + "  pk = " + str(pk))
        # return "remind task()" + "  self = " + str(self) + "  pk = " + str(pk)
        return

    except Exception as e:
        self.retry(exc=e)


@celery.task(
    bind=True,# ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def digest(self):
    return "digest task()" + "  self = " + str(self)
    # find the start and end of this week
    year, week = datetime.datetime.now().isocalendar()[0:2]
    date = datetime.date(year, 1, 1)
    if (date.weekday() > 3):
        date = date + datetime.timedelta(7 - date.weekday())
    else:
        date = date - datetime.timedelta(date.weekday())
    delta = datetime.timedelta(days=(week - 1) * 7)
    start, end = date + delta, date + delta + datetime.timedelta(days=6)

    posts = Post.query.filter(
        Post.publish_date >= start,
        Post.publish_date <= end
    ).all()

    if (len(posts) == 0):
        return

    msg = MIMEText(render_template("digest.html", posts=posts), 'html')

    msg['Subject'] = "Weekly Digest"
    msg['From'] = ""

    try:
        smtp_server = smtplib.SMTP('localhost')
        smtp_server.starttls()
        # smtp_server.login(user, password)
        smtp_server.sendmail("", [""], msg.as_string())
        smtp_server.close()

        return
    except Exception as e:
        self.retry(exc=e)

def on_reminder_save(mapper, connect, self):

    #ok
    # debug("on_reminder_save()")
    # result = log.apply_async(args=(["log->msg"]))
    # debug(str(result.ready()) + "  " + str(result.get()))

    #ok
    # debug("on_reminder_save()")
    # result = m.apply_async(args=(111,3))
    # debug(str(result.ready()) + "  " + str(result.get()))

    #ok
    # debug("on_reminder_save()")
    # result = xx_new_comment.apply_async(args=(111,3))
    # debug(str(result.ready()) + "  " + str(result.get()))

    debug("on_reminder_save()")
    result = remind.apply_async(args=(self.id,))            #(self.id,) "," 必需要
    debug(str(result.ready()) + str(result.get()))

