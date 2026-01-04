# 🏫 نظام إدارة الحضانة (Crèche Management System)

تطبيق ويب مبني باستخدام Flask لإدارة الحضانات والروضات.

## 📋 نظرة عامة

هذا النظام يوفر منصة شاملة لإدارة عمليات الحضانة اليومية، بما في ذلك إدارة الأطفال، الموظفين، والأنشطة.

## ✨ الميزات

- 👶 إدارة بيانات الأطفال
- 👨‍👩‍👧‍👦 إدارة بيانات أولياء الأمور
- 👥 إدارة الموظفين
- 📅 جدولة الأنشطة
- 📊 لوحة تحكم إدارية
- 🔐 نظام تسجيل دخول آمن

## 🛠️ التقنيات المستخدمة

- **Backend**: Flask (Python)
- **Database**: MongoDB (NoSQL)
- **ODM**: PyMongo / MongoEngine
- **Frontend**: HTML, CSS
- **Architecture**: MVC Pattern

## 📁 هيكل المشروع

```
crecheWAPP/
│
├── controllers/        # معالجات الطلبات والمنطق
├── models/            # نماذج قاعدة البيانات
├── templates/         # قوالب HTML
├── app.py            # نقطة الدخول الرئيسية
├── db.py             # إعدادات قاعدة البيانات
└── requirements.txt  # المكتبات المطلوبة
```

## 🚀 التثبيت والإعداد

### المتطلبات الأساسية

- Python 3.8 أو أحدث
- pip (مدير حزم Python)
- MongoDB 4.0 أو أحدث
- MongoDB Compass (اختياري للإدارة المرئية)

### خطوات التثبيت

1. **استنساخ المستودع**
   ```bash
   git clone https://github.com/monalhoms-arch/crecheWAPP.git
   cd crecheWAPP
   ```

2. **إنشاء بيئة افتراضية**
   ```bash
   python -m venv venv
   
   # على Windows
   venv\Scripts\activate
   
   # على Linux/Mac
   source venv/bin/activate
   ```

3. **تثبيت المكتبات المطلوبة**
   ```bash
   pip install -r requirements.txt
   ```

4. **تشغيل MongoDB**
   ```bash
   # تأكد من تشغيل MongoDB على جهازك
   # على Windows
   mongod
   
   # على Linux/Mac
   sudo systemctl start mongod
   # أو
   brew services start mongodb-community
   ```

5. **إعداد قاعدة البيانات**
   ```bash
   # سيتم إنشاء قاعدة البيانات تلقائياً عند أول تشغيل
   python db.py
   ```

6. **تشغيل التطبيق**
   ```bash
   python app.py
   ```

7. **فتح المتصفح**
   ```
   افتح المتصفح وانتقل إلى: http://localhost:5000
   ```

## 🔧 الإعدادات

يمكنك تخصيص الإعدادات في ملف `app.py`:

- تغيير المنفذ (Port)
- إعدادات الاتصال بـ MongoDB (URI, Database Name)
- مفتاح السرية (Secret Key)
- وضع التطوير/الإنتاج

### مثال على إعدادات MongoDB

```python
# في ملف db.py أو app.py
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "creche_db"
```

## 📝 الاستخدام

### تسجيل الدخول

1. قم بزيارة الصفحة الرئيسية
2. أدخل بيانات الدخول
3. ستتم إعادة توجيهك إلى لوحة التحكم

### إدارة الأطفال

- إضافة طفل جديد
- تحديث بيانات الأطفال
- عرض سجل الحضور
- إدارة الأنشطة

### إدارة الموظفين

- إضافة موظف جديد
- تحديث بيانات الموظفين
- إدارة الصلاحيات

## 🤝 المساهمة

نرحب بمساهماتك! يرجى اتباع الخطوات التالية:

1. Fork المشروع
2. إنشاء فرع جديد (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى الفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## 🐛 الإبلاغ عن المشاكل

إذا واجهت أي مشاكل، يرجى فتح [Issue](https://github.com/monalhoms-arch/crecheWAPP/issues) جديد مع:
- وصف المشكلة
- خطوات إعادة الإنتاج
- لقطات الشاشة (إن وجدت)

### مشاكل شائعة

**المشكلة**: لا يمكن الاتصال بـ MongoDB
```bash
# الحل: تأكد من تشغيل MongoDB
mongod --version
# وتحقق من أن MongoDB يعمل على المنفذ الافتراضي 27017
```

## 📄 الترخيص

هذا المشروع مفتوح المصدر ومتاح للاستخدام الحر.

## 👨‍💻 المطور

**Monal Homs**
- GitHub: [@monalhoms-arch](https://github.com/monalhoms-arch)

## 📞 الدعم

للحصول على الدعم:
- فتح Issue في GitHub
- التواصل عبر البريد الإلكتروني

## 🔄 التحديثات المستقبلية

- [ ] إضافة نظام الإشعارات
- [ ] تطبيق الهاتف المحمول
- [ ] تقارير متقدمة
- [ ] نظام الرسائل
- [ ] دعم متعدد اللغات

---

⭐ إذا أعجبك هذا المشروع، لا تنسى إعطائه نجمة على GitHub!