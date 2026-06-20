from datetime import datetime

def convert_to_amadeus_date(day_num, month_num, year_str=None):
    """تحويل أرقام اليوم والشهر إلى صيغة أماديوس (مثل: 30APR)"""
    months_dict = {
        1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
        7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"
    }
    month_letter = months_dict[int(month_num)]
    day_padded = str(day_num).zfill(2)
    
    if year_str:
        year_short = str(year_str)[-2:]
        return f"{day_padded}{month_letter}{year_short}"
    else:
        return f"{day_padded}{month_letter}"

def amadeus_helper():
    print("=== نظام الأنفمس المطور بالكامل ⚡ (نسخة الاختصارات السريعة y/n) ===")
    
    # -----------------------------------------------------------------
    # 1️⃣ مرحلة البحث عن الرحلات واختيار الدرجة
    # -----------------------------------------------------------------
    print("\n🛫 [1. مرحلة البحث عن الرحلة]")
    day_out = input("📅 رقم يوم الذهاب (1-31): ").strip()
    month_out = input("📅 رقم شهر الذهاب (1-12): ").strip()
    from_city = input("🛫 من (مثال JED): ").strip().upper()
    to_city = input("🛬 إلى (مثال RUH): ").strip().upper()
    
    print("💺 [اختيار درجة السفر]")
    cabin_class = input("   أدخل حرف الدرجة (Y ضيافة / C أعمال / F أولى): ").strip().upper()
    
    try:
        date_out_formatted = convert_to_amadeus_date(day_out, month_out)
    except (ValueError, KeyError):
        print("❌ خطأ في إدخال أرقام التاريخ!")
        return

    an_go_command = f"AN {date_out_formatted} {from_city} {to_city}/A SV/K {cabin_class}"
    print("👉 كود بحث الذهاب جاهز للنسخ")
    print(f"{an_go_command}")
    print("-" * 40)

    # تعديل الاختصار ليكون y أو n فقط 🎯
    has_return = input("🔄 هل توجد رحلة عودة؟ (y / n): ").strip().lower() == 'y'
    if has_return:
        day_ret = input("📅 رقم يوم العودة (1-31): ").strip()
        month_ret = input("📅 رقم شهر العودة (1-12): ").strip()
        try:
            date_ret_formatted = convert_to_amadeus_date(day_ret, month_ret)
            an_return_command = f"AN {date_ret_formatted} {to_city} {from_city}/A SV/K {cabin_class}"
            print("👉 كود بحث العودة جاهز للنسخ")
            print(f"{an_return_command}")
        except (ValueError, KeyError):
            print("❌ خطأ في إدخال تاريخ العودة!")
            return
    print("=" * 50)

    # -----------------------------------------------------------------
    # 2️⃣ مرحلة حساب التكلفة والباقات (قبل الأسماء)
    # -----------------------------------------------------------------
    print("\n👥 [2. مرحلة حساب التكلفة والباقات]")
    adult_count = int(input("👨 كم عدد البالغين؟ ").strip())
    
    child_count = 0
    # تعديل الاختصار ليكون y أو n فقط 🎯
    has_child = input("👦 هل يوجد أطفال؟ (y / n): ").strip().lower() == 'y'
    if has_child:
        child_count = int(input("   كم عدد الأطفال؟ ").strip())
        
    infant_count = 0
    # تعديل الاختصار ليكون y أو n فقط 🎯
    has_infant = input("👶 هل يوجد رضع؟ (y / n): ").strip().lower() == 'y'
    if has_infant:
        infant_count = int(input("   كم عدد الرضع؟ ").strip())
        if infant_count > adult_count:
            print(f"⚠️ تنبيه نظامي: عدد الرضع أكبر من البالغين!")
            return

    print("\n📋 أوامر التسعير الفورية (انسخها وشيك السعر)")
    print("👉 للبالغين")
    print("FXX")
    if child_count > 0: 
        print("👉 للأطفال")
        print("FXX/RCHD")
    if infant_count > 0: 
        print("👉 للرضع")
        print("FXX/RINF")
    print("=" * 50)

    # -----------------------------------------------------------------
    # 3️⃣ مرحلة جمع بيانات الركاب والأسماء
    # -----------------------------------------------------------------
    print("\n👤 [3. مرحلة جمع بيانات الركاب]")
    all_passengers = []
    assigned_infants = 0
    
    # جمع البالغين والرضع
    for i in range(1, adult_count + 1):
        print(f"\n📝 بيانات البالغ رقم {i}:")
        p_last = input("لقب العائلة (Last Name): ").strip().upper()
        p_first = input("الاسم الأول (First Name): ").strip().upper()
        p_title = input("صفة الضيف (MR / MS): ").strip().upper()
        
        infant_data = None
        if assigned_infants < infant_count:
            assigned_infants += 1
            print(f"👶 ربط رضيع تلقائياً مع البالغ رقم {i}:")
            inf_last = input("   اسم عائلة الرضيع: ").strip().upper()
            inf_first = input("   الاسم الأول للرضيع: ").strip().upper()
            inf_day = input("   يوم ميلاد الرضيع: ").strip()
            inf_month = input("   شهر ميلاد الرضيع: ").strip()
            inf_year = input("   سنة ميلاد الرضيع: ").strip()
            inf_dob = convert_to_amadeus_date(inf_day, inf_month, inf_year)
            infant_data = {'last': inf_last, 'first': inf_first, 'dob': inf_dob}
            
        all_passengers.append({
            'type': 'ADT', 'last': p_last, 'first': p_first, 'title': p_title, 'infant': infant_data
        })

    # جمع الأطفال
    for j in range(1, child_count + 1):
        print(f"\n📝 بيانات الطفل رقم {j}:")
        ch_last = input("اسم عائلة الطفل: ").strip().upper()
        ch_first = input("الاسم الأول للطفل: ").strip().upper()
        ch_gender = input("هل الطفل (ولد / بنت): ").strip()
        ch_title = "MSTR" if ch_gender in ['ولد', 'm', 'boy'] else "MISS"
        ch_day = input("يوم ميلاد الطفل: ").strip()
        ch_month = input("شهر ميلاد الطفل: ").strip()
        ch_year = input("سنة ميلاد الطفل: ").strip()
        ch_dob = convert_to_amadeus_date(ch_day, ch_month, ch_year)
        
        all_passengers.append({
            'type': 'CHD', 'last': ch_last, 'first': ch_first, 'title': ch_title, 'dob': ch_dob
        })

    # ترتيب المسافرين أبجدياً (A-Z)
    all_passengers.sort(key=lambda x: (x['last'], x['first']))
    total_passengers_count = len(all_passengers)

    if total_passengers_count > 1:
        pax_range = f"P1-{total_passengers_count}"
    else:
        pax_range = "P1"

    # طباعة أوامر الأسماء بالتسلسل الأبجدي
    print("\n📋 أوامر إدخال الأسماء (مرتبة أبجدياً وجاهزة للنسخ سطر بسطر)")
    for idx, pax in enumerate(all_passengers, start=1):
        if pax['type'] == 'ADT':
            if pax['infant']:
                cmd = f"NM1 {pax['last']}/{pax['first']} {pax['title']}(INF {pax['infant']['last']}/{pax['infant']['first']}/{pax['infant']['dob']})"
            else:
                cmd = f"NM1 {pax['last']}/{pax['first']} {pax['title']}"
        else:  # CHD
            cmd = f"NM1 {pax['last']}/{pax['first']} {pax['title']}(CHD/{pax['dob']})"
            
        print(f"👉 الراكب رقم {idx} ({pax['type']})")
        print(f"{cmd}")
        pax['id_in_system'] = idx 
        print("-" * 30)
    print("=" * 50)

    # -----------------------------------------------------------------
    # 4️⃣ مرحلة إدخال الاتصال الشامل (APN + APM + APE) بالنطاق التلقائي
    # -----------------------------------------------------------------
    print("\n📞 [4. مرحلة إدخال الاتصال والبيانات الأساسية]")
    phone_num = input("📱 أدخل رقم جوال العميل: ").strip()
    email_input = input("📧 أدخل إيميل العميل (مثال: saud@mail.com): ").strip().lower()
    
    email_formatted = email_input.replace('@', '//').replace('_', '..')

    print(f"\n📋 أوامر الاتصال جاهزة للنسخ (مربوطة تلقائياً بالركاب {pax_range})")
    print("👉 أمر إدخال رقم الجوال في النظام (APN)")
    print(f"APN-SV/M+966{phone_num}/AR/{pax_range}")
    print("👉 أمر إرسال الرسالة النصية والتنبيهات للعميل (APM)")
    print(f"APM-SV/M+966{phone_num}/AR/{pax_range}")
    print("👉 أمر إدخال الإيميل (APE)")
    print(f"APE-{email_formatted}")
    print("=" * 50)

    # -----------------------------------------------------------------
    # 5️⃣ مرحلة وثائق السفر (SR DOCS) مع ذكاء فحص الهوية الوطنية
    # -----------------------------------------------------------------
    print("\n🛂 [5. مرحلة إدخال وثائق السفر SR DOCS - بالترتيب الأبجدي]")
    docs_commands = []
    
    for pax in all_passengers:
        name_for_display = f"{pax['last']}/{pax['first']}"
        print(f"\n📑 وثيقة السفر للراكب: {name_for_display} (سطر P{pax['id_in_system']})")
        
        doc_type = input("نوع الوثيقة (P للجواز / I للهوية الوطنية): ").strip().upper()
        doc_num = input("رقم الوثيقة/الجواز/الهوية: ").strip().upper()
        nationality = input("الجنسية (مثال SA): ").strip().upper()
        gender = input("الجنس (M للذكر / F للأنثى): ").strip().upper()
        
        if doc_type == "I":
            docs_cmd = f"SR DOCS SV HK1-{doc_type}-{nationality}-{doc_num}-{nationality}--{gender}-{name_for_display}/P{pax['id_in_system']}"
        else:
            doc_day = input("يوم انتهاء الجواز: ").strip()
            doc_month = input("شهر انتهاء الجواز: ").strip()
            doc_year = input("سنة انتهاء الجواز: ").strip()
            doc_exp = convert_to_amadeus_date(doc_day, doc_month, doc_year)
            docs_cmd = f"SR DOCS SV HK1-{doc_type}-{nationality}-{doc_num}-{nationality}-{doc_exp}-{gender}-EXP DATE-{name_for_display}/P{pax['id_in_system']}"
            
        docs_commands.append(docs_cmd)
        
        if pax['type'] == 'ADT' and pax['infant']:
            inf_name = f"{pax['infant']['last']}/{pax['infant']['first']}"
            print(f"   👶 وثيقة السفر للرضيع المرتفق: {inf_name}")
            inf_doc_type = input("   نوع وثيقة الرضيع (P للجواز / I للهوية): ").strip().upper()
            inf_doc_num = input("   رقم الوثيقة للرضيع: ").strip().upper()
            inf_gender = "MI" if gender == "M" else "FI"
            
            if inf_doc_type == "I":
                inf_docs_cmd = f"SR DOCS SV HK1-{inf_doc_type}-{nationality}-{inf_doc_num}-{nationality}--{inf_gender}-{inf_name}/P{pax['id_in_system']}"
            else:
                inf_doc_day = input("   يوم انتهاء جواز الرضيع: ").strip()
                inf_doc_month = input("   شهر انتهاء جواز الرضيع: ").strip()
                inf_doc_year = input("   سنة انتهاء جواز الرضيع: ").strip()
                inf_doc_exp = convert_to_amadeus_date(inf_doc_day, inf_doc_month, inf_doc_year)
                inf_docs_cmd = f"SR DOCS SV HK1-{inf_doc_type}-{nationality}-{inf_doc_num}-{nationality}-{inf_doc_exp}-{inf_gender}-EXP DATE-{inf_name}/P{pax['id_in_system']}"
                
            docs_commands.append(inf_docs_cmd)

    print("\n📋 أوامر وثائق السفر جاهزة للنسخ بالتتابع والأبجدية الصحيحة")
    for d_cmd in docs_commands:
        print(f"{d_cmd}")
    print("=" * 50)

    # -----------------------------------------------------------------
    # 6️⃣ مرحلة تقفيل وإنهاء الحجز وحساب سداد واستعراض التذاكر
    # -----------------------------------------------------------------
    print("\n💳 [6. مرحلة التثبيت النهائي وإصدار رقم سداد]")
    print("📋 أوامر التقفيل الأولية والتوقيع (انسخها بالترتيب)")
    print("👉 كود إدخال نظام التذاكر")
    print("TKOK")
    print("👉 كود الحفظ الأولي (التوقيع)")
    print("RFF . ER . ER")
    print("-" * 30)
    
    print("\n💳 أوامر التثبيت وباقة الفرسان/الحكومي وصناعة الفاتورة")
    print("👉 لتثبيت السعر أو الباقة")
    print("FXP/FF")
    print("👉 لتحديد طريقة الدفع (سداد)")
    print("FP SADAD")
    print("👉 كود الحفظ الثاني والأخير")
    print("RFF . ER . ER")
    print("👉 لتصدير الحجز النهائي وظهور رقم سداد")
    print("TTP/RT")
    print("👉 لمعرفة مهلة أو وقت السداد المتوقع")
    print("RTO")
    print("-" * 30)

    print("\n🎫 أوامر استعراض وفتح التذاكر الإلكترونية (خطوات المدرب زياد)")
    print("👉 لاستعراض التذاكر المرفقة بالملف")
    print("RTF")
    print("👉 لفتح التذكرة واستعراض كامل تفاصيلها")
    print("TWD/L")
    print("=" * 60)
    print("\n✨ تم التحديث بنجاح! السكربت صار أسرع في التشغيل ولا يتطلب إلا حرف واحد للإجابة.")

if __name__ == "__main__":
    amadeus_helper()