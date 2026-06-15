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
    print("=== نظام الأنفمس التفاعلي الشامل ⚡ (إصدار سعود المطور) ===")
    current_year = datetime.now().year
    
    # -----------------------------------------------------------------
    # 1️⃣ مرحلة البحث عن الرحلات (الذهاب والعودة)
    # -----------------------------------------------------------------
    print("\n🛫 [1. مرحلة البحث عن الرحلة]")
    day_out = input("📅 رقم يوم الذهاب (1-31): ").strip()
    month_out = input("📅 رقم شهر الذهاب (1-12): ").strip()
    from_city = input("🛫 من (مثال JED): ").strip().upper()
    to_city = input("🛬 إلى (مثال RUH): ").strip().upper()
    
    try:
        date_out_formatted = convert_to_amadeus_date(day_out, month_out)
    except (ValueError, KeyError):
        print("❌ خطأ في إدخال أرقام التاريخ!")
        return

    # النتيجة الفورية للذهاب 🎯
    an_go_command = f"AN {date_out_formatted} {from_city} {to_city}/A SV"
    print(f"👉 كود بحث الذهاب جاهز للنسخ: {an_go_command}")
    print("-" * 40)

    # تشيك العودة فوراً
    has_return = input("🔄 هل توجد رحلة عودة؟ (نعم / لا): ").strip() in ['نعم', 'y', 'yes', 'يب']
    if has_return:
        day_ret = input("📅 رقم يوم العودة (1-31): ").strip()
        month_ret = input("📅 رقم شهر العودة (1-12): ").strip()
        try:
            date_ret_formatted = convert_to_amadeus_date(day_ret, month_ret)
            # النتيجة الفورية للعودة 🎯
            an_return_command = f"AN {date_ret_formatted} {to_city} {from_city}/A SV"
            print(f"👉 كود بحث العودة جاهز للنسخ: {an_return_command}")
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
    has_child = input("👦 هل يوجد أطفال؟ (نعم / لا): ").strip() in ['نعم', 'y', 'yes', 'يب']
    if has_child:
        child_count = int(input("   كم عدد الأطفال؟ ").strip())
        
    infant_count = 0
    has_infant = input("👶 هل يوجد رضع؟ (نعم / لا): ").strip() in ['نعم', 'y', 'yes', 'يب']
    if has_infant:
        infant_count = int(input("   كم عدد الرضع؟ ").strip())
        if infant_count > adult_count:
            print(f"⚠️ تنبيه نظامي: عدد الرضع أكبر من البالغين! لا يمكن الإكمال.")
            return

    # النتيجة الفورية للتسعير والباقات 🎯
    print("\n📋 أوامر التسعير الفورية (انسخها وشيك السعر):")
    print(f"👉 للبالغين: FXX")
    if child_count > 0: 
        print(f"👉 للأطفال: FXX/RCHD")
    if infant_count > 0: 
        print(f"👉 للرضع: FXX/RINF")
    print("=" * 50)

    # -----------------------------------------------------------------
    # 3️⃣ مرحلة إدخال الأسماء (سطر بسطر ونتيجة فورية)
    # -----------------------------------------------------------------
    print("\n👤 [3. مرحلة إدخال الأسماء - سطر بسطر]")
    
    assigned_infants = 0
    
    # أسماء البالغين والرضع
    for i in range(1, adult_count + 1):
        print(f"\n📝 بيانات البالغ رقم {i}:")
        p_last = input("لقب العائلة (Last Name): ").strip().upper()
        p_first = input("الاسم الأول (First Name): ").strip().upper()
        p_title = input("صفة الضيف (MR / MS): ").strip().upper()
        
        # ربط الرضيع تلقائياً فوراً لو باقي رضع
        if assigned_infants < infant_count:
            assigned_infants += 1
            print(f"👶 ربط الرضيع رقم {assigned_infants} تلقائياً:")
            inf_last = input("   اسم عائلة الرضيع: ").strip().upper()
            inf_first = input("   الاسم الأول للرضيع: ").strip().upper()
            inf_day = input("   يوم ميلاد الرضيع: ").strip()
            inf_month = input("   شهر ميلاد الرضيع: ").strip()
            inf_year = input("   سنة ميلاد الرضيع (مثال 2026): ").strip()
            inf_dob = convert_to_amadeus_date(inf_day, inf_month, inf_year)
            
            p_cmd = f"NM1 {p_last}/{p_first} {p_title}(INF {inf_last}/{inf_first}/{inf_dob})"
        else:
            p_cmd = f"NM1 {p_last}/{p_first} {p_title}"
            
        # النتيجة الفورية لاسم البالغ الحالي 🎯
        print(f"👉 انسخ كود هذا الاسم فوراً للسيستم: {p_cmd}")
        print("-" * 40)

    # أسماء الأطفال
    for j in range(1, child_count + 1):
        print(f"\n📝 بيانات الطفل رقم {j}:")
        ch_last = input("اسم عائلة الطفل: ").strip().upper()
        ch_first = input("الاسم الأول للطفل: ").strip().upper()
        ch_gender = input("هل الطفل (ولد / بنت): ").strip()
        ch_title = "MSTR" if ch_gender in ['ولد', 'm', 'boy'] else "MISS"
        ch_day = input("يوم ميلاد الطفل: ").strip()
        ch_month = input("شهر ميلاد الطفل: ").strip()
        ch_year = input("سنة ميلاد الطفل (مثال 2020): ").strip()
        ch_dob = convert_to_amadeus_date(ch_day, ch_month, ch_year)
        
        ch_cmd = f"NM1 {ch_last}/{ch_first} {ch_title}(CHD/{ch_dob})"
        
        # النتيجة الفورية لاسم الطفل الحالي 🎯
        print(f"👉 انسخ كود اسم الطفل فوراً للسيستم: {ch_cmd}")
        print("-" * 40)
    print("=" * 50)

    # -----------------------------------------------------------------
    # 4️⃣ مرحلة تقفيل وإنهاء الحجز (البيانات الإضافية المدمجة) 🎯
    # -----------------------------------------------------------------
    print("\n📞 [4. مرحلة إنهاء وتقفيل الحجز]")
    phone_num = input("📱 أدخل رقم جوال العميل للاتصال: ").strip()
    
    print("\n📋 الأكواد النهائية لتقفيل الملف في الأماديوس (انسخها بالترتيب):")
    print(f"👉 كود إدخال الجوال: AP {phone_num}")
    print(f"👉 كود إصدار وتأكيد التذاكر: TK OK")
    print(f"👉 كود التوقيع والمرجع (بإسمك): RFF SAUD")
    print(f"👉 كود الحفظ النهائي والإنهاء: ER")
    print("=" * 50)

    print("\n✨ تم الانتهاء من إعداد الحجز وتجهيز كافة الأكواد بنجاح.")

if __name__ == "__main__":
    amadeus_helper()