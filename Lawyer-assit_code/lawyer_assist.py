from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import os
import gradio as gr

os.environ["OPENAI_API_KEY"] = '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'
os.environ["OPENAI_API_KEY_2"] = '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'

# 定义第一个 prompt 用于处理对话
prompt1 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "请扮演律师的角色小A,负责与咨询人进行沟通收集咨询人的信息，认真负责，耐心提问，给咨询人良好的体验"
        "按照文档中的信息依次向咨询人提出问题，一次只提一个问题"
        "咨询者及受伤职工基本信息,工伤事件细节,劳动合同情况,薪资及保险,救治和医疗情况,休养与薪资发放情况,离职情况,工伤和劳动能力鉴定,职业病情况"
    ),
    MessagesPlaceholder(variable_name="history"), HumanMessagePromptTemplate.from_template("{input}")
])

# 定义第二个 prompt 用于整理信息
prompt2 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "请扮演一位律师助理的角色，名字是小I，不负责提问，只要整理信息"
        "相关表单信息格式如下：作为输出的格式，严格按照下列表单输出，每句话后回车，每次输出已经知道的确切信息"
        "# 工伤案件咨询信息整理"
        "## 1. 咨询者及受伤职工基本信息"
        "- **咨询人的身份信息**- **咨询人与受伤职工的关系** 或 **咨询人与受伤职工用人单位的关系**- **受伤职工的身份信息**：是否属于外地来沪从业人员？- **受伤职工用人单位的信息**：是否属于建筑施工、矿山企业？- **受伤职工与用人单位的关系信息**：是否属于灵活就业等特殊用工？"
        "## 2. 工伤事件细节"
        "- **工作岗位和职责**- **伤害发生的时间、地点**- **伤害的具体过程** 及 **与工作的关系**- **单位的考勤方式**- 若涉及第三人侵权，**第三人侵权责任的认定**"
        "## 3. 劳动合同情况"
        "- 是否签订**劳动合同**？  - 若已签订，关注以下内容：    - 合同签订主体    - 合同履行地    - 合同期限    - 工资    - 岗位等信息  - 若未签订，了解以下内容：    - 用人单位与所有员工是否均未签订劳动合同？    - 是否有证明受伤职工与用人单位存在劳动关系的证据？"
        "## 4. 薪资及保险"
        "- **工作岗位**- **工资标准**- **工资发放方式**- **用人单位工伤保险费缴纳情况**  - 是否缴纳工伤保险费？  - 工伤保险的类型  - 缴费标准"
        "## 5. 救治和医疗情况"
        "- **受伤人员的送医过程**及**救治情况**- 护理人员情况- 是否跨地区治疗？- **支付的医药费数额**、付款记录及票据是否保留？- 治疗费用是否由用人单位支付？"
        "## 6. 休养与薪资发放情况"
        "- **停工休养时长**- 是否请病假？假条是否已提供给用人单位？- 用人单位是否准许请假？- 停工留薪期间工资发放情况"
        "## 7. 离职情况"
        "- 是否已离职？- 离职时间- 离职手续办理情况- 离职时是否得到用人单位补偿？若是，补偿的名目及数额？- 双方是否签订协议"
        "## 8. 工伤和劳动能力鉴定"
        "- 工伤是否已申报？- 申报主体- 申报结果- 鉴定结果- 是否已收到工伤待遇款项？"
        "## 9. 职业病情况"
        "- 若职工患有职业病，需要了解病情、诊断及鉴定情况"
        "## 10. 其他相关信息"
        "- 与工伤案件有关的其他具体信息"),
    MessagesPlaceholder(variable_name="history"), HumanMessagePromptTemplate.from_template("{input}")
])

llm1 = ChatOpenAI(temperature=0.5, api_key=os.environ["OPENAI_API_KEY"])
llm2 = ChatOpenAI(temperature=0.1, api_key=os.environ["OPENAI_API_KEY_2"])
memory = ConversationBufferMemory(return_messages=True)

# 创建两个不同的 ConversationChain 对象，分别用于处理对话和整理信息
conversation1 = ConversationChain(memory=memory, prompt=prompt1, llm=llm1)
conversation2 = ConversationChain(memory=memory, prompt=prompt2, llm=llm2)

conversation_history = []


def predict(input_text):
    global conversation_history
    conversation_history.append(input_text)
    history_text = '[SEP]'.join(conversation_history)
    input_text = history_text + '[SEP]' + input_text
    output = conversation1.predict(input=input_text)
    table1 = conversation2.predict(input=input_text)
    return output, table1


iface = gr.Interface(fn=predict, inputs='text', outputs=['text', 'text'])
history = gr.State([])
iface.launch()

# 案例如下：
'''
我是叶，想咨询工伤问题

我是受伤职工本人，不是外地来沪的，是一家软件公司上班，不属于你说的建筑矿山企业，是灵活就业，就是实习期间
岗位是软件测试，负责黑盒测试，去医院查出腰部有了损害，办公室久坐的原因，考勤是通过钉钉
我是实习生，劳动合同不太清楚欸....我再去问问情况，已经实习一个月了，总共是要3个月的，

没有签，那个好像没有法律效益...就是一个承诺书，感觉我以后自己多注意注意吧，谢谢律师

'''
