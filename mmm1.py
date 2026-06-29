import streamlit as st
import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Anfms Amadeus Helper", page_icon="✈️", layout="centered")

def to_amadeus_date(date_obj):
    if not date_obj:
        return ""
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    day = str(date_obj.day).zfill(2)
    month = months[date_obj.month - 1]
    return f"{day}{month}"

def to_amadeus_dob_short(date_obj):
    if not date_obj:
        return ""
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    day = str(date_obj.day).zfill(2)
    month = months[date_obj.month - 1]
    year_short = str(date_obj.year)[-2:]
    return f"{day}{month}{year_short}"

def mobile_date_picker(label, default_val, key):
    st.markdown(f"**{label}**")
    js_code = f"""
    <input type="date" id="{key}" value="{default_val}" 
    style="width: 100%; padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;"
    onchange="parent.postMessage({{type: 'date_changed', key: '{key}', value: this.value}}, '*')">
    """
    components.html(js_code, height=45)
    if key not in st.session_state:
        st.session_state[key] = default_val
    date_str = st.session_state[key]
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return datetime.date.today()

st.title("⚡ نظام ابو عامر اتصل نصل")
st.write("أدخل البيانات في الخانات بالأسفل، وستظهر لك الأكواد مرتبة بالتسلسل الدقيق والمطابق تماماً لخطوات الحجز!")
st.markdown("---")

current_year = datetime.date.today().year

# ════════════════════════════════════════════
# نوع الحجز: عادي أم فرسان
# ════════════════════════════════════════════
st.subheader("🎯 0. نوع الحجز")
booking_type = st.radio("اختر نوع الحجز:", ["✈️ حجز عادي (نقدي/بطاقة)", "🏅 حجز فرسان (أميال)"])
is_fursan = "فرسان" in booking_type

st.markdown("---")

# ════════════════════════════════════════════
# 1. تفاصيل الرحلة والتسعير
# ════════════════════════════════════════════
st.subheader("🛫 1. تفاصيل الرحلة والتسعير")
col1, col2 = st.columns(2)
with col1:
    from_city = st.text_input("🛫 من (مثال: JED)", "JED").upper()
    date_out = st.date_input("📅 تاريخ الذهاب")
with col2:
    to_city = st.text_input("🛬 إلى (مثال: RUH)", "RUH").upper()
    has_return = st.checkbox("🔄 إضافة رحلة عودة")
    date_ret = None
    if has_return:
        date_ret = st.date_input("📅 تاريخ العودة")

col3, col4 = st.columns(2)
with col3:
    if is_fursan:
        cabin_class = st.selectbox("💺 درجة السفر", ["X (ضيافة فرسان)", "O (أعمال فرسان)", "A (أولى فرسان)"])
    else:
        cabin_class = st.selectbox("💺 درجة السفر", ["Y (ضيافة)", "C (أعمال)", "F (أولى)"])
    class_letter = cabin_class.split()[0]

with col4:
    if not is_fursan:
        if class_letter == "Y":
            fare_basis = st.selectbox("💰 باقة التسعير (الضيافة)", ["NSAVERE (سيفير)", "NBASICE (بيسك)", "NFLEXE (فليكس)"])
        elif class_letter == "C":
            fare_basis = st.selectbox("💰 باقة التسعير (الأعمال)", ["NBASICB (بيسك)", "NFLEXB (فليكس)"])
        else:
            fare_basis = st.selectbox("💰 باقة التسعير (الأولى)", ["NFLEXF (فليكس)"])
        fare_suffix = fare_basis.split()[0]
    else:
        fare_suffix = "FURSAN2"

# ━━━━ نوع التسعير (اعتماد / اتفاقية) — للحجز العادي فقط
if not is_fursan:
    st.markdown("**🏷️ نوع التسعير:**")
    pricing_type = st.radio(
        "اختر نوع التسعير:",
        [
            "💼 تسعير اعتماد عادي (NGR26)",
            "🤝 تسعير اتفاقية بين الطيران السعودي وطيران آخر (GOV)",
        ],
        horizontal=True,
    )
    if "NGR26" in pricing_type:
        fxx_cmd = "FXX/R,U*NGR26"
        fxp_cmd_suffix = "FXP/R,U*NGR26"
    else:
        fxx_cmd = "FXX/R,U*GOV"
        fxp_cmd_suffix = "FXP/R,U*GOV"
else:
    fxx_cmd = "FXX"
    fxp_cmd_suffix = "FXP/R,U*FURSAN2"

st.markdown("---")

# ════════════════════════════════════════════
# قسم الفرسان التفصيلي
# ════════════════════════════════════════════
fursan_membership = ""
fursan_card_type = ""
fursan_free_code = ""
fursan_booking_status = ""

if is_fursan:
    st.subheader("🏅 1أ. بيانات عضوية الفرسان")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fursan_membership = st.text_input("رقم عضوية الفرسان", "1234567890")
    with col_f2:
        num_pax_fursan = st.number_input("عدد الركاب على هذه العضوية (P)", min_value=1, max_value=9, value=1)

    st.markdown("**💳 نوع بطاقة الدفع (بعد RTF):**")
    card_options = {
        "VISA": "VI",
        "MasterCard": "CA",
        "American Express": "AX",
        "Diners Club": "DC",
        "JCB": "JC",
    }
    fursan_card_name = st.selectbox("اختر نوع البطاقة", list(card_options.keys()))
    fursan_card_type = card_options[fursan_card_name]

    col_f3, col_f4 = st.columns(2)
    with col_f3:
        fursan_pax_line = st.text_input("رقم سطر المسافر (بعد RTF)", "1")
    with col_f4:
        fursan_price = st.text_input("السعر بالريال (SAR)", "0")

    st.markdown("**🎫 الأكواد المجانية (اختياري):**")
    free_code_options = {
        "لا يوجد": "",
        "UPGRD — ترقية مجانية": "UPGRD",
        "STPC — وجبة/إقامة مجانية": "STPC",
        "EXBG — حقيبة إضافية مجانية": "EXBG",
        "MAAS — مساعدة في المطار": "MAAS",
        "WCHR — كرسي متحرك": "WCHR",
        "SPML — وجبة خاصة": "SPML",
    }
    fursan_free_label = st.selectbox("اختر الكود المجاني المطلوب", list(free_code_options.keys()))
    fursan_free_code = free_code_options[fursan_free_label]

    st.markdown("**📌 حالة الحجز (Status):**")
    status_options = {
        "HK — مؤكد (Confirmed)": "HK",
        "HL — قائمة الانتظار (Waitlist)": "HL",
        "TK — مؤكد بتغيير (Ticketing OK after change)": "TK",
        "UN — غير مؤكد (Unable to confirm)": "UN",
        "NO — لم يتم الحجز (Not Operating)": "NO",
        "SC — جدولة مغلقة (Schedule Change)": "SC",
    }
    fursan_status_label = st.selectbox("اختر حالة الحجز", list(status_options.keys()))
    fursan_booking_status = status_options[fursan_status_label]

    st.markdown("---")

# ════════════════════════════════════════════
# 2. أعداد المسافرين
# ════════════════════════════════════════════
st.subheader("👥 2. أعداد المسافرين")
col5, col6, col7 = st.columns(3)
with col5:
    adult_count = st.number_input("👨 عدد البالغين", min_value=1, max_value=9, value=1)
with col6:
    child_count = st.number_input("👦 عدد الأطفال", min_value=0, max_value=9, value=0)
with col7:
    infant_count = st.number_input("👶 عدد الرضع", min_value=0, max_value=9, value=0)

total_pax = adult_count + child_count
pax_range = f"P1-{total_pax}" if total_pax > 1 else "P1"

st.markdown("---")

# ════════════════════════════════════════════
# 3. بيانات الاتصال
# ════════════════════════════════════════════
st.subheader("📞 3. بيانات الاتصال ولغة الإشعار")
col_lang, col_phone, col_email = st.columns(3)
with col_lang:
    pax_lang = st.selectbox("🌐 لغة الرسائل للعميل", ["AR (العربية)", "EN (الإنجليزي)"])
    lang_code = pax_lang.split()[0]
with col_phone:
    phone_num = st.text_input("📱 رقم الجوال (بدون صفر)", "500000000")
with col_email:
    email_input = st.text_input("📧 إيميل العميل", "saud@gmail.com").lower()

st.markdown("---")

# ════════════════════════════════════════════
# 4. وثائق السفر
# ════════════════════════════════════════════
st.subheader("🛂 4. وثائق السفر للركاب")
pax_docs_list = []

for i in range(1, adult_count + 1):
    st.markdown(f"#### 👨 بيانات الراكب البالغ رقم {i}")
    c_ln, c_fn = st.columns(2)
    with c_ln:
        last_name = st.text_input(f"لقب العائلة للبالغ {i}", "SMITH", key=f"p_ln_{i}").upper()
    with c_fn:
        first_name = st.text_input(f"الاسم الأول للبالغ {i}", "JOHN", key=f"p_fn_{i}").upper()

    pax_dob_date = mobile_date_picker(f"📅 تاريخ ميلاد البالغ {i}", "1995-01-01", f"p_dob_val_{i}")
    pax_dob_str = to_amadeus_dob_short(pax_dob_date)

    c_dt, c_dn, c_g = st.columns(3)
    with c_dt:
        doc_type = st.selectbox(f"نوع الوثيقة للبالغ {i}", ["I (هوية وطنية)", "P (جواز سفر)", "A (إقامة)"], key=f"p_dt_{i}").split()[0]
    with c_dn:
        doc_num = st.text_input(f"رقم الوثيقة للبالغ {i}", "1000000000", key=f"p_dn_{i}").upper()
    with c_g:
        gender = st.selectbox(f"الجنس للبالغ {i}", ["M (ذكر)", "F (أنثى)"], key=f"p_g_{i}").split()[0]

    doc_exp_str = ""
    if doc_type in ["P", "A"]:
        doc_exp_date = mobile_date_picker(f"📅 تاريخ انتهاء وثيقة البالغ {i}", f"{current_year+5}-01-01", f"p_exp_val_{i}")
        doc_exp_str = to_amadeus_date(doc_exp_date)

    pax_docs_list.append({
        'type': 'ADT', 'last': last_name, 'first': first_name,
        'title': 'MR' if gender == 'M' else 'MS',
        'doc_type': doc_type, 'doc_num': doc_num, 'gender': gender,
        'exp': doc_exp_str, 'dob': pax_dob_str, 'infant': None
    })

assigned_infants = 0
for idx, pax in enumerate(pax_docs_list):
    if assigned_infants < infant_count and pax['type'] == 'ADT':
        assigned_infants += 1
        st.markdown(f"#### 👶 ربط وثيقة الرضيع المرتفق مع البالغ رقم {idx+1}")
        i_ln, i_fn = st.columns(2)
        with i_ln:
            inf_last = st.text_input(f"عائلة الرضيع {assigned_infants}", pax['last'], key=f"inf_ln_{assigned_infants}").upper()
        with i_fn:
            inf_first = st.text_input(f"الاسم الأول للرضيع {assigned_infants}", "BABY", key=f"inf_fn_{assigned_infants}").upper()

        inf_dob_date = mobile_date_picker(f"📅 تاريخ ميلاد الرضيع {assigned_infants}", f"{current_year}-01-01", f"inf_dob_val_{assigned_infants}")
        inf_dob_str = to_amadeus_dob_short(inf_dob_date)

        i_dt, i_dn = st.columns(2)
        with i_dt:
            inf_doc_type = st.selectbox(f"نوع وثيقة الرضيع {assigned_infants}", ["I (هوية)", "P (جواز)", "A (إقامة)"], key=f"inf_dt_{assigned_infants}").split()[0]
        with i_dn:
            inf_doc_num = st.text_input(f"رقم وثيقة الرضيع {assigned_infants}", "2000000000", key=f"inf_dn_{assigned_infants}").upper()

        inf_exp_str = ""
        if inf_doc_type in ["P", "A"]:
            inf_exp_date = mobile_date_picker(f"📅 تاريخ انتهاء وثيقة الرضيع {assigned_infants}", f"{current_year+5}-01-01", f"inf_exp_val_{assigned_infants}")
            inf_exp_str = to_amadeus_date(inf_exp_date)

        pax['infant'] = {
            'last': inf_last, 'first': inf_first, 'doc_type': inf_doc_type,
            'doc_num': inf_doc_num, 'dob': inf_dob_str, 'exp': inf_exp_str,
            'gender': 'MI' if pax['gender'] == 'M' else 'FI'
        }

for j in range(1, child_count + 1):
    st.markdown(f"#### 👦 بيانات وثيقة الراكب الطفل رقم {j}")
    ch_ln, ch_fn = st.columns(2)
    with ch_ln:
        ch_last = st.text_input(f"عائلة الطفل {j}", "SMITH", key=f"ch_ln_{j}").upper()
    with ch_fn:
        ch_first = st.text_input(f"الاسم الأول للطفل {j}", "BOY", key=f"ch_fn_{j}").upper()

    ch_dob_date = mobile_date_picker(f"📅 تاريخ ميلاد الطفل {j}", f"{current_year-5}-01-01", f"ch_dob_val_{j}")
    ch_dob_str = to_amadeus_dob_short(ch_dob_date)

    ch_dt, ch_dn, ch_g = st.columns(3)
    with ch_dt:
        ch_doc_type = st.selectbox(f"نوع وثيقة الطفل {j}", ["I (هوية وطنية)", "P (جواز سفر)", "A (إقامة)"], key=f"ch_dt_{j}").split()[0]
    with ch_dn:
        ch_doc_num = st.text_input(f"رقم وثيقة الطفل {j}", "3000000000", key=f"ch_dn_{j}").upper()
    with ch_g:
        ch_gender = st.selectbox(f"جنس الطفل {j}", ["M (ذكر)", "F (أنثى)"], key=f"ch_g_{j}").split()[0]

    ch_exp_str = ""
    if ch_doc_type in ["P", "A"]:
        ch_exp_date = mobile_date_picker(f"📅 تاريخ انتهاء وثيقة الطفل {j}", f"{current_year+5}-01-01", f"ch_exp_val_{j}")
        ch_exp_str = to_amadeus_date(ch_exp_date)

    pax_docs_list.append({
        'type': 'CHD', 'last': ch_last, 'first': ch_first,
        'title': 'MSTR' if ch_gender == 'M' else 'MISS',
        'doc_type': ch_doc_type, 'doc_num': ch_doc_num, 'gender': ch_gender,
        'exp': ch_exp_str, 'dob': ch_dob_str, 'infant': None
    })

pax_docs_list.sort(key=lambda x: (x['last'], x['first']))

st.markdown("---")

# ════════════════════════════════════════════
# 5. طريقة الدفع (للحجز العادي فقط)
# ════════════════════════════════════════════
pay_cmd = ""
if not is_fursan:
    st.subheader("💳 5. طريقة الدفع المعتمدة")
    pay_method = st.radio("اختر طريقة الدفع:", ["SADAD (نظام سداد)", "MOBIP (رابط موبيباي الإلكتروني)", "CREDIT CARD (البطاقة الائتمانية)"])
    pay_cmd = "FP SADAD" if "SADAD" in pay_method else ("FP MOBIP" if "MOBIP" in pay_method else "FP CC")
    st.markdown("---")

# ════════════════════════════════════════════
# شاشة الأوامر النهائية
# ════════════════════════════════════════════
st.header("📋 شاشة الأوامر النهائية")

# 1. أوامر البحث AN
date_out_formatted = to_amadeus_date(date_out)
st.text_area("👉 أمر البحث عن رحلة الذهاب (AN):", f"AN {date_out_formatted} {from_city} {to_city}/A SV/K {class_letter}", height=70)

if has_return and date_ret:
    date_ret_formatted = to_amadeus_date(date_ret)
    st.text_area("👉 أمر البحث عن رحلة العودة (AN):", f"AN {date_ret_formatted} {to_city} {from_city}/A SV/K {class_letter}", height=70)

# 2. أوامر الأسعار والتشييك
if is_fursan:
    pricing_preview_cmds = [fxx_cmd]
    if child_count > 0:
        pricing_preview_cmds.append(f"{fxx_cmd}/RCHD")
    if infant_count > 0:
        pricing_preview_cmds.append(f"{fxx_cmd}/RINF")
else:
    pricing_preview_cmds = [fxx_cmd]
    if child_count > 0:
        pricing_preview_cmds.append(f"{fxx_cmd}/RCHD")
    if infant_count > 0:
        pricing_preview_cmds.append(f"{fxx_cmd}/RINF")

st.text_area("👉 أوامر استعراض الأسعار (FXX):", "\n".join(pricing_preview_cmds), height=110)

# 3. أوامر الأسماء
names_commands = []
for idx, p in enumerate(pax_docs_list, start=1):
    p['sys_id'] = idx
    if is_fursan:
        # في الفرسان نستخدم FFASV
        if p['type'] == 'ADT':
            if p['infant']:
                names_commands.append(f"NM1 {p['last']}/{p['first']} {p['title']}(INF {p['infant']['last']}/{p['infant']['first']}/{p['infant']['dob']})")
            else:
                names_commands.append(f"NM1 {p['last']}/{p['first']} {p['title']}")
        else:
            names_commands.append(f"NM1 {p['last']}/{p['first']} {p['title']}(CHD/{p['dob']})")
    else:
        if p['type'] == 'ADT':
            if p['infant']:
                names_commands.append(f"NM1 {p['last']}/{p['first']} {p['title']}(INF {p['infant']['last']}/{p['infant']['first']}/{p['infant']['dob']})")
            else:
                names_commands.append(f"NM1 {p['last']}/{p['first']} {p['title']}")
        else:
            names_commands.append(f"NM1 {p['last']}/{p['first']} {p['title']}(CHD/{p['dob']})")

st.text_area("👉 أوامر إدخال الأسماء (أبجدية متسلسلة):", "\n".join(names_commands), height=120)

# 4. أوامر عضوية الفرسان (إن وجدت)
if is_fursan and fursan_membership:
    fursan_cmds = []
    for p_idx in range(1, adult_count + child_count + 1):
        fursan_cmds.append(f"FFASV-{fursan_membership}/P{p_idx}")
    # إضافة خصم الأميال لكل مسافر
    for p_idx in range(1, adult_count + child_count + 1):
        fursan_cmds.append(f"FFRSV-{fursan_membership}/P{p_idx}")
    st.text_area("👉 أوامر عضوية الفرسان وخصم الأميال (FFASV / FFRSV):", "\n".join(fursan_cmds), height=130)

# 5. أوامر الاتصال
contact_cmds = [
    f"APM-SV/M+966{phone_num}/{lang_code}/{pax_range}",
    f"APN-SV/M+966{phone_num}/{lang_code}/{pax_range}",
    f"APE-{email_input}"
]
st.text_area("👉 أوامر الاتصال والرسائل والإيميل (APM, APN, APE):", "\n".join(contact_cmds), height=110)

# 6. وثائق السفر + الإغلاق النهائي
docs_cmds = []
for p in pax_docs_list:
    name_str = f"{p['last']}/{p['first']}"
    if p['doc_type'] == 'I':
        docs_cmds.append(f"SR DOCS SV HK1-{p['doc_type']}-SA-{p['doc_num']}-SA-{p['dob']}-{p['gender']}--{name_str}/P{p['sys_id']}")
    else:
        docs_cmds.append(f"SR DOCS SV HK1-{p['doc_type']}-SA-{p['doc_num']}-SA-{p['dob']}-{p['gender']}-{p['exp']}-{name_str}/P{p['sys_id']}")

    if p['infant']:
        inf = p['infant']
        inf_name = f"{inf['last']}/{inf['first']}"
        if inf['doc_type'] == 'I':
            docs_cmds.append(f"SR DOCS SV HK1-{inf['doc_type']}-SA-{inf['doc_num']}-SA-{inf['dob']}-{inf['gender']}--{inf_name}/P{p['sys_id']}")
        else:
            docs_cmds.append(f"SR DOCS SV HK1-{inf['doc_type']}-SA-{inf['doc_num']}-SA-{inf['dob']}-{inf['gender']}-{inf['exp']}-{inf_name}/P{p['sys_id']}")

# بناء الإغلاق حسب نوع الحجز
if is_fursan:
    # كود الكود المجاني إن وجد
    free_code_line = f"SR {fursan_free_code} SV HK1" if fursan_free_code else ""
    # سطر حالة الحجز
    status_line = f"ST {fursan_booking_status}" if fursan_booking_status else ""

    final_parts = [
        "TKOK",
        "RFF . ER . ER",
        "",
        "[أوامر وثائق السفر المتكاملة]:",
        "\n".join(docs_cmds),
        "",
        "RFF . ER . ER",
        fxp_cmd_suffix,
        "FXM",
    ]
    if free_code_line:
        final_parts.append(free_code_line)
    if status_line:
        final_parts.append(status_line)
    final_parts += [
        "RFF . ER . ER",
        "RTF",
        f"({fursan_pax_line}/+CC{fursan_card_type}/SAR{fursan_price})",
        "RTO",
        "RTF",
        "TWD/L",
    ]
else:
    final_parts = [
        "TKOK",
        "RFF . ER . ER",
        "",
        "[أوامر وثائق السفر المتكاملة]:",
        "\n".join(docs_cmds),
        "",
        "RFF . ER . ER",
        "FXP",
        f"{fxp_cmd_suffix}/FF-{fare_suffix}",
        pay_cmd,
        "RFF . ER . ER",
        "TTP/RT",
        "RTO",
        "RTF",
        "TWD/L",
    ]

st.text_area("👉 خطوات الحفظ والتثبيت والدفع والتذاكر النهائية:", "\n".join(final_parts), height=400)
