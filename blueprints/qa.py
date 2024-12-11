import contextlib
import io
from venv import logger

from flask import Blueprint, request, render_template, g, redirect, url_for, jsonify
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel, ChatRecord
from exts import db, handler
from decorators import login_required

bp = Blueprint("qa", __name__, url_prefix="/")


# http://127.0.0.1:5000
@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html", questions=questions)


@bp.route("/qa/public", methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo: 跳转到这篇问答的详情页
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))


@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)


# @bp.route("/answer/public", methods=['POST'])
@bp.post("/answer/public")
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))


@bp.route("/search")
@login_required
def search():
    # /search?q=flask
    # /search/<q>
    # post, request.form
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("index.html", questions=questions)


    # questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    # return render_template("index.html", questions=questions)

@bp.route('/chat', methods=['POST','GET'])
@login_required
def chat():
    return render_template('chat.html')

@bp.route('/chat_main', methods=['POST'])
def chat_main():
    question = request.form['question']
    logger.info(f"收到问题: {question}")

    if question.lower() in ('跪安', '退下', '结束', '退出', 'end', '再见'):
        logger.info("结束对话")
        return jsonify({'answer': '本次问答到此结束，期待下次为您服务~~~'})

    try:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            # 假设 handler.chat_main 是一个函数，用于处理聊天逻辑
            handler.chat_main(question)

        answer = output.getvalue().strip()
        logger.info(f"生成的答案: {answer}")

        chat_record = ChatRecord(question=question, answer=answer, author_id=g.user.id)
        db.session.add(chat_record)
        db.session.commit()

        if answer:
            return jsonify({'answer': answer})
        else:
            logger.warning("未生成答案")
            answer = "无答案"
            return jsonify({'answer': "小冰不知道哦，小冰会努力学习哒~"})
            # 保存对话记录到数据库

    except Exception as e:
        logger.error(f"处理问题时发生错误: {str(e)}", exc_info=True)
        return jsonify({'answer': "抱歉，处理您的问题时出现了错误。请稍后再试。"})
