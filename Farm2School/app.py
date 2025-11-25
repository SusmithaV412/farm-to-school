from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime
from flask_mail import Mail, Message as MailMessage

app = Flask(__name__)
app.secret_key = 'farm2school_secret_key'

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'susmitha.vcsc@gmail.com'
app.config['MAIL_PASSWORD'] = 'abcd efgh ijkl mnop'  # Replace with your actual 16-character Gmail app password
app.config['MAIL_DEFAULT_SENDER'] = 'susmitha.vcsc@gmail.com'

mail = Mail(app)

# MongoDB configuration
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['farm2school']
    users = db['users']
    products = db['products']
    orders = db['orders']
    message_collection = db['messages']
    print("MongoDB connected successfully")
except Exception as e:
    print(f"MongoDB connection error: {str(e)}")

# Translations
translations = {
    'en': {
        'title': 'Farm2School - Connecting Farms to Schools',
        'tagline': 'Fresh • Local • Sustainable',
        'nav': {
            'home': 'Home',
            'about': 'About',
            'how_it_works': 'How It Works',
            'features': 'Features',
            'contact': 'Contact',
            'login': 'Login',
            'register': 'Register'
        },
        'hero': {
            'title': 'Connecting Fresh Farms to Schools',
            'subtitle': 'Building healthier communities by connecting local farms with schools',
            'get_started': 'Get Started',
            'learn_more': 'Learn More'
        },
        'about': {
            'title': 'About Farm2School',
            'subtitle': 'Building healthier communities by connecting local farms with schools',
            'description1': 'Farm2School is a revolutionary platform that bridges the gap between local farmers and educational institutions. We believe in providing students with access to fresh, nutritious, and locally-sourced food while supporting small-scale farmers in our communities.',
            'description2': 'Our mission is to create sustainable food systems that benefit everyone involved - farmers get fair prices for their produce, schools receive fresh ingredients, and students enjoy healthier meals that contribute to their overall well-being.'
        },
        'how_it_works': {
            'title': 'How It Works',
            'subtitle': 'A simple process connecting farms to schools',
            'step1': {'title': 'Register', 'description': 'Farmers and schools create accounts on our platform with their details and requirements.'},
            'step2': {'title': 'List & Browse', 'description': 'Farmers list their available produce, and schools browse through the available options.'},
            'step3': {'title': 'Order', 'description': 'Schools place orders for the fresh produce they need directly from local farmers.'},
            'step4': {'title': 'Deliver', 'description': 'Farmers deliver fresh produce to schools, and payments are processed securely.'}
        },
        'features': {
            'title': 'Platform Features',
            'subtitle': 'Tools designed to make farm-to-school connections seamless',
            'feature1': {'title': 'Fresh Produce', 'description': 'Access to the freshest locally-grown fruits, vegetables, and dairy products.'},
            'feature2': {'title': 'Direct Connection', 'description': 'Eliminate middlemen and connect directly with local farmers and schools.'},
            'feature3': {'title': 'Real-time Tracking', 'description': 'Track orders from placement to delivery with our real-time tracking system.'},
            'feature4': {'title': 'Sustainability', 'description': 'Promote environmentally-friendly practices and reduce food miles.'},
            'feature5': {'title': 'Educational Resources', 'description': 'Access educational materials about farming, nutrition, and sustainability.'},
            'feature6': {'title': 'Mobile Friendly', 'description': 'Access the platform from any device with our responsive design.'}
        },
        'contact': {
            'title': 'Contact Us',
            'subtitle': 'Have questions? We\'d love to hear from you',
            'address': {'title': 'Address', 'value': 'Thudiyalur, Coimbatore'},
            'phone': {'title': 'Phone'},
            'email': {'title': 'Email'},
            'form': {'name': 'Your Name', 'email': 'Your Email', 'message': 'Your Message', 'send': 'Send Message'}
        },
        'footer': {
            'tagline': 'Connecting farms to schools for a healthier future',
            'quick_links': 'Quick Links',
            'follow_us': 'Follow Us',
            'rights': 'All rights reserved.'
        },
        'login': {
            'title': 'Welcome Back',
            'subtitle': 'Login to your Farm2School account',
            'email': 'Email Address',
            'password': 'Password',
            'remember': 'Remember me',
            'forgot': 'Forgot password?',
            'login_btn': 'Login',
            'no_account': "Don't have an account?",
            'register_here': 'Register here'
        },
        'register': {
            'title': 'Create Account',
            'subtitle': 'Join Farm2School to connect farms and schools',
            'user_type': 'I am a:',
            'farmer': 'Farmer',
            'farmer_desc': 'I want to sell my produce',
            'school': 'School',
            'school_desc': 'I want to buy fresh produce',
            'name': 'Name',
            'email': 'Email Address',
            'district': 'District',
            'location': 'Specific Location/Address',
            'password': 'Password',
            'register_btn': 'Register',
            'have_account': 'Already have an account?',
            'login_here': 'Login here'
        },
        'dashboard': {
            'farmer': {
                'title': 'Farmer Dashboard',
                'schools_in_district': 'Schools in Your District',
                'your_products': 'Your Products',
                'orders': 'Orders',
                'add_product': 'Add Product',
                'product_name': 'Product Name',
                'description': 'Description',
                'price': 'Price (₹)',
                'quantity': 'Quantity (in kgs)',
                'category': 'Category',
                'contact': 'Contact',
                'delete': 'Delete',
                'out_of_stock': 'Out of Stock'
            },
            'school': {
                'title': 'School Dashboard',
                'farmers_in_district': 'Farmers in Your District',
                'available_products': 'Available Products',
                'your_orders': 'Your Orders',
                'order': 'Order',
                'filter': 'Filter',
                'clear': 'Clear'
            },
            'common': {
                'home': 'Home',
                'dashboard': 'Dashboard',
                'messages': 'Messages',
                'analytics': 'Analytics',
                'logout': 'Logout',
                'products_listed': 'Products Listed',
                'total_orders': 'Total Orders',
                'delivered_orders': 'Delivered Orders'
            }
        }
    },
    'ta': {
        'title': 'Farm2School - பண்ணைகளை பள்ளிகளுடன் இணைக்கிறது',
        'tagline': 'புதிய • உள்ளூர் • நிலையான',
        'nav': {
            'home': 'முகப்பு',
            'about': 'எங்களைப் பற்றி',
            'how_it_works': 'எப்படி வேலை செய்கிறது',
            'features': 'அம்சங்கள்',
            'contact': 'தொடர்பு',
            'login': 'உள்நுழைய',
            'register': 'பதிவு செய்ய'
        },
        'hero': {
            'title': 'புதிய பண்ணைகளை பள்ளிகளுடன் இணைக்கிறது',
            'subtitle': 'உள்ளூர் பண்ணைகளை பள்ளிகளுடன் இணைத்து ஆரோக்கியமான சமுதாயங்களை உருவாக்குதல்',
            'get_started': 'தொடங்குங்கள்',
            'learn_more': 'மேலும் அறிய'
        },
        'about': {
            'title': 'Farm2School பற்றி',
            'subtitle': 'உள்ளூர் பண்ணைகளை பள்ளிகளுடன் இணைத்து ஆரோக்கியமான சமுதாயங்களை உருவாக்குதல்',
            'description1': 'Farm2School என்பது உள்ளூர் விவசாயிகளுக்கும் கல்வி நிறுவனங்களுக்கும் இடையிலான இடைவெளியைக் குறைக்கும் ஒரு புரட்சிகர தளமாகும். எங்கள் சமுதாயங்களில் உள்ள சிறிய அளவிலான விவசாயிகளை ஆதரிக்கும் அதே வேளையில் மாணவர்களுக்கு புதிய, சத்தான மற்றும் உள்ளூர் உணவுகளை வழங்குவதில் நாங்கள் நம்புகிறோம்.',
            'description2': 'சம்பந்தப்பட்ட அனைவருக்கும் பயனளிக்கும் நிலையான உணவு அமைப்புகளை உருவாக்குவதே எங்கள் நோக்கம் - விவசாயிகள் தங்கள் விளைபொருட்களுக்கு நியாயமான விலையைப் பெறுகிறார்கள், பள்ளிகள் புதிய பொருட்களைப் பெறுகின்றன, மாணவர்கள் அவர்களின் ஒட்டுமொத்த நல்வாழ்வுக்கு பங்களிக்கும் ஆரோக்கியமான உணவுகளை அனுபவிக்கிறார்கள்.'
        },
        'how_it_works': {
            'title': 'எப்படி வேலை செய்கிறது',
            'subtitle': 'பண்ணைகளை பள்ளிகளுடன் இணைக்கும் எளிய செயல்முறை',
            'step1': {'title': 'பதிவு செய்ய', 'description': 'விவசாயிகள் மற்றும் பள்ளிகள் தங்கள் விவரங்கள் மற்றும் தேவைகளுடன் எங்கள் தளத்தில் கணக்குகளை உருவாக்குகின்றன.'},
            'step2': {'title': 'பட்டியல் மற்றும் உலாவல்', 'description': 'விவசாயிகள் தங்கள் கிடைக்கக்கூடிய விளைபொருட்களை பட்டியலிடுகிறார்கள், பள்ளிகள் கிடைக்கக்கூடிய விருப்பங்களை உலாவுகின்றன.'},
            'step3': {'title': 'ஆர்டர்', 'description': 'பள்ளிகள் உள்ளூர் விவசாயிகளிடமிருந்து நேரடியாக தங்களுக்குத் தேவையான புதிய விளைபொருட்களுக்கு ஆர்டர் செய்கின்றன.'},
            'step4': {'title': 'விநியோகம்', 'description': 'விவசாயிகள் பள்ளிகளுக்கு புதிய விளைபொருட்களை வழங்குகிறார்கள், பணம் செலுத்துதல் பாதுகாப்பாக செயல்படுத்தப்படுகிறது.'}
        },
        'features': {
            'title': 'தள அம்சங்கள்',
            'subtitle': 'பண்ணை-பள்ளி இணைப்புகளை தடையற்றதாக மாற்ற வடிவமைக்கப்பட்ட கருவிகள்',
            'feature1': {'title': 'புதிய விளைபொருட்கள்', 'description': 'புதிய உள்ளூர் பழங்கள், காய்கறிகள் மற்றும் பால் பொருட்களை அணுகுதல்.'},
            'feature2': {'title': 'நேரடி இணைப்பு', 'description': 'இடைத்தரகர்களை நீக்கி உள்ளூர் விவசாயிகள் மற்றும் பள்ளிகளுடன் நேரடியாக இணைக்கவும்.'},
            'feature3': {'title': 'நிகழ்நேர கண்காணிப்பு', 'description': 'எங்கள் நிகழ்நேர கண்காணிப்பு அமைப்புடன் ஆர்டர் செய்வதிலிருந்து விநியோகம் வரை கண்காணிக்கவும்.'},
            'feature4': {'title': 'நிலைத்தன்மை', 'description': 'சுற்றுச்சூழல் நட்பு நடைமுறைகளை ஊக்குவித்து உணவு மைல்களை குறைக்கவும்.'},
            'feature5': {'title': 'கல்வி வளங்கள்', 'description': 'விவசாயம், ஊட்டச்சத்து மற்றும் நிலைத்தன்மை பற்றிய கல்வி பொருட்களை அணுகவும்.'},
            'feature6': {'title': 'மொபைல் நட்பு', 'description': 'எங்கள் பதிலளிக்கக்கூடிய வடிவமைப்புடன் எந்த சாதனத்திலிருந்தும் தளத்தை அணுகவும்.'}
        },
        'contact': {
            'title': 'எங்களை தொடர்பு கொள்ளுங்கள்',
            'subtitle': 'கேள்விகள் உள்ளதா? உங்களிடமிருந்து கேட்க விரும்புகிறோம்',
            'address': {'title': 'முகவரி', 'value': 'துடியலூர், கோயம்புத்தூர்'},
            'phone': {'title': 'தொலைபேசி'},
            'email': {'title': 'மின்னஞ்சல்'},
            'form': {'name': 'உங்கள் பெயர்', 'email': 'உங்கள் மின்னஞ்சல்', 'message': 'உங்கள் செய்தி', 'send': 'செய்தி அனுப்பு'}
        },
        'footer': {
            'tagline': 'ஆரோக்கியமான எதிர்காலத்திற்காக பண்ணைகளை பள்ளிகளுடன் இணைக்கிறது',
            'quick_links': 'விரைவு இணைப்புகள்',
            'follow_us': 'எங்களை பின்தொடருங்கள்',
            'rights': 'அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை.'
        },
        'login': {
            'title': 'மீண்டும் வரவேற்கிறோம்',
            'subtitle': 'உங்கள் Farm2School கணக்கில் உள்நுழையுங்கள்',
            'email': 'மின்னஞ்சல் முகவரி',
            'password': 'கடவுச்சொல்',
            'remember': 'என்னை நினைவில் வைத்துக்கொள்ளுங்கள்',
            'forgot': 'கடவுச்சொல் மறந்துவிட்டதா?',
            'login_btn': 'உள்நுழைய',
            'no_account': 'கணக்கு இல்லையா?',
            'register_here': 'இங்கே பதிவு செய்யுங்கள்'
        },
        'register': {
            'title': 'கணக்கு உருவாக்கவும்',
            'subtitle': 'பண்ணைகளை பள்ளிகளுடன் இணைக்க Farm2School இல் சேருங்கள்',
            'user_type': 'நான் ஒரு:',
            'farmer': 'விவசாயி',
            'farmer_desc': 'நான் என் விளைபொருட்களை விற்க விரும்புகிறேன்',
            'school': 'பள்ளி',
            'school_desc': 'நான் புதிய விளைபொருட்களை வாங்க விரும்புகிறேன்',
            'name': 'பெயர்',
            'email': 'மின்னஞ்சல் முகவரி',
            'district': 'மாவட்டம்',
            'location': 'குறிப்பிட்ட இடம்/முகவரி',
            'password': 'கடவுச்சொல்',
            'register_btn': 'பதிவு செய்யுங்கள்',
            'have_account': 'ஏற்கனவே கணக்கு உள்ளதா?',
            'login_here': 'இங்கே உள்நுழையுங்கள்'
        },
        'dashboard': {
            'farmer': {
                'title': 'விவசாயி டாஷ்போர்டு',
                'schools_in_district': 'உங்கள் மாவட்டத்தில் உள்ள பள்ளிகள்',
                'your_products': 'உங்கள் பொருட்கள்',
                'orders': 'ஆர்டர்கள்',
                'add_product': 'பொருள் சேர்க்கவும்',
                'product_name': 'பொருளின் பெயர்',
                'description': 'விளக்கம்',
                'price': 'விலை (₹)',
                'quantity': 'அளவு (கிலோவில்)',
                'category': 'வகை',
                'contact': 'தொடர்பு',
                'delete': 'நீக்கு',
                'out_of_stock': 'கையிருப்பு இல்லை'
            },
            'school': {
                'title': 'பள்ளி டாஷ்போர்டு',
                'farmers_in_district': 'உங்கள் மாவட்டத்தில் உள்ள விவசாயிகள்',
                'available_products': 'கிடைக்கும் பொருட்கள்',
                'your_orders': 'உங்கள் ஆர்டர்கள்',
                'order': 'ஆர்டர்',
                'filter': 'வடிகட்டு',
                'clear': 'அழிக்கவும்'
            },
            'common': {
                'home': 'முகப்பு',
                'dashboard': 'டாஷ்போர்டு',
                'messages': 'செய்திகள்',
                'analytics': 'பகுப்பாய்வு',
                'logout': 'வெளியேறு',
                'products_listed': 'பட்டியலிடப்பட்ட பொருட்கள்',
                'total_orders': 'மொத்த ஆர்டர்கள்',
                'delivered_orders': 'வழங்கப்பட்ட ஆர்டர்கள்'
            }
        }
    },
    'hi': {
        'title': 'Farm2School - खेतों को स्कूलों से जोड़ना',
        'tagline': 'ताज़ा • स्थानीय • टिकाऊ',
        'nav': {
            'home': 'होम',
            'about': 'हमारे बारे में',
            'how_it_works': 'यह कैसे काम करता है',
            'features': 'विशेषताएं',
            'contact': 'संपर्क',
            'login': 'लॉगिन',
            'register': 'रजिस्टर'
        },
        'hero': {
            'title': 'ताज़े खेतों को स्कूलों से जोड़ना',
            'subtitle': 'स्थानीय खेतों को स्कूलों से जोड़कर स्वस्थ समुदाय बनाना',
            'get_started': 'शुरू करें',
            'learn_more': 'और जानें'
        },
        'about': {
            'title': 'Farm2School के बारे में',
            'subtitle': 'स्थानीय खेतों को स्कूलों से जोड़कर स्वस्थ समुदाय बनाना',
            'description1': 'Farm2School एक क्रांतिकारी प्लेटफॉर्म है जो स्थानीय किसानों और शैक्षणिक संस्थानों के बीच की खाई को पाटता है। हम छात्रों को ताज़े, पौष्टिक और स्थानीय रूप से उगाए गए भोजन तक पहुंच प्रदान करने में विश्वास करते हैं जबकि हमारे समुदायों में छोटे पैमाने के किसानों का समर्थन करते हैं।',
            'description2': 'हमका मिशन टिकाऊ खाद्य प्रणालियां बनाना है जो सभी शामिल लोगों को लाभ पहुंचाती हैं - किसानों को उनकी उपज के लिए उचित मूल्य मिलता है, स्कूलों को ताज़ी सामग्री मिलती है, और छात्र स्वस्थ भोजन का आनंद लेते हैं जो उनकी समग्र भलाई में योगदान देता है।'
        },
        'how_it_works': {
            'title': 'यह कैसे काम करता है',
            'subtitle': 'खेतों को स्कूलों से जोड़ने की एक सरल प्रक्रिया',
            'step1': {'title': 'रजिस्टर करें', 'description': 'किसान और स्कूल अपने विवरण और आवश्यकताओं के साथ हमारे प्लेटफॉर्म पर खाते बनाते हैं।'},
            'step2': {'title': 'सूची और ब्राउज़', 'description': 'किसान अपनी उपलब्ध उपज की सूची बनाते हैं, और स्कूल उपलब्ध विकल्पों को ब्राउज़ करते हैं।'},
            'step3': {'title': 'ऑर्डर', 'description': 'स्कूल स्थानीय किसानों से सीधे अपनी आवश्यक ताज़ी उपज के लिए ऑर्डर देते हैं।'},
            'step4': {'title': 'डिलीवरी', 'description': 'किसान स्कूलों को ताज़ी उपज पहुंचाते हैं, और भुगतान सुरक्षित रूप से संसाधित होता है।'}
        },
        'features': {
            'title': 'प्लेटफॉर्म विशेषताएं',
            'subtitle': 'खेत-से-स्कूल कनेक्शन को निर्बाध बनाने के लिए डिज़ाइन किए गए उपकरण',
            'feature1': {'title': 'ताज़ी उपज', 'description': 'सबसे ताज़े स्थानीय रूप से उगाए गए फल, सब्जियां और डेयरी उत्पादों तक पहुंच।'},
            'feature2': {'title': 'प्रत्यक्ष कनेक्शन', 'description': 'बिचौलियों को हटाएं और स्थानीय किसानों और स्कूलों से सीधे जुड़ें।'},
            'feature3': {'title': 'रियल-टाइम ट्रैकिंग', 'description': 'हमारे रियल-टाइम ट्रैकिंग सिस्टम के साथ ऑर्डर प्लेसमेंट से डिलीवरी तक ट्रैक करें।'},
            'feature4': {'title': 'स्थिरता', 'description': 'पर्यावरण-अनुकूल प्रथाओं को बढ़ावा दें और खाद्य मील कम करें।'},
            'feature5': {'title': 'शैक्षिक संसाधन', 'description': 'खेती, पोषण और स्थिरता के बारे में शैक्षिक सामग्री तक पहुंच।'},
            'feature6': {'title': 'मोबाइल फ्रेंडली', 'description': 'हमारे रिस्पॉन्सिव डिज़ाइन के साथ किसी भी डिवाइस से प्लेटफॉर्म तक पहुंचें।'}
        },
        'contact': {
            'title': 'हमसे संपर्क करें',
            'subtitle': 'प्रश्न हैं? हम आपसे सुनना पसंद करेंगे',
            'address': {'title': 'पता', 'value': 'थुडियालुर, कोयंबटूर'},
            'phone': {'title': 'फोन'},
            'email': {'title': 'ईमेल'},
            'form': {'name': 'आपका नाम', 'email': 'आपका ईमेल', 'message': 'आपका संदेश', 'send': 'संदेश भेजें'}
        },
        'footer': {
            'tagline': 'स्वस्थ भविष्य के लिए खेतों को स्कूलों से जोड़ना',
            'quick_links': 'त्वरित लिंक',
            'follow_us': 'हमें फॉलो करें',
            'rights': 'सभी अधिकार सुरक्षित।'
        },
        'login': {
            'title': 'वापस स्वागत है',
            'subtitle': 'अपने Farm2School खाते में लॉगिन करें',
            'email': 'ईमेल पता',
            'password': 'पासवर्ड',
            'remember': 'मुझे याद रखें',
            'forgot': 'पासवर्ड भूल गए?',
            'login_btn': 'लॉगिन',
            'no_account': 'खाता नहीं है?',
            'register_here': 'यहाँ रजिस्टर करें'
        },
        'register': {
            'title': 'खाता बनाएं',
            'subtitle': 'खेतों और स्कूलों को जोड़ने के लिए Farm2School में शामिल हों',
            'user_type': 'मैं हूँ:',
            'farmer': 'किसान',
            'farmer_desc': 'मैं अपनी उपज बेचना चाहता हूँ',
            'school': 'स्कूल',
            'school_desc': 'मैं ताज़ी उपज खरीदना चाहता हूँ',
            'name': 'नाम',
            'email': 'ईमेल पता',
            'district': 'जिला',
            'location': 'विशिष्ट स्थान/पता',
            'password': 'पासवर्ड',
            'register_btn': 'रजिस्टर करें',
            'have_account': 'पहले से खाता है?',
            'login_here': 'यहाँ लॉगिन करें'
        },
        'dashboard': {
            'farmer': {
                'title': 'किसान डैशबोर्ड',
                'schools_in_district': 'आपके जिले में स्कूल',
                'your_products': 'आपके उत्पाद',
                'orders': 'ऑर्डर',
                'add_product': 'उत्पाद जोड़ें',
                'product_name': 'उत्पाद का नाम',
                'description': 'विवरण',
                'price': 'मूल्य (₹)',
                'quantity': 'मात्रा (किलो में)',
                'category': 'श्रेणी',
                'contact': 'संपर्क',
                'delete': 'हटाएं',
                'out_of_stock': 'स्टॉक में नहीं'
            },
            'school': {
                'title': 'स्कूल डैशबोर्ड',
                'farmers_in_district': 'आपके जिले में किसान',
                'available_products': 'उपलब्ध उत्पाद',
                'your_orders': 'आपके ऑर्डर',
                'order': 'ऑर्डर',
                'filter': 'फिल्टर',
                'clear': 'साफ़ करें'
            },
            'common': {
                'home': 'होम',
                'dashboard': 'डैशबोर्ड',
                'messages': 'संदेश',
                'analytics': 'एनालिटिक्स',
                'logout': 'लॉगआउट',
                'products_listed': 'सूचीबद्ध उत्पाद',
                'total_orders': 'कुल ऑर्डर',
                'delivered_orders': 'डिलीवर किए गए ऑर्डर'
            }
        }
    }
}

# Routes
@app.route('/')
def index():
    return render_template('language_select.html')

@app.route('/home')
def home():
    lang = request.args.get('lang', 'en')
    if lang not in translations:
        lang = 'en'
    return render_template('index_multilingual.html', lang=lang, translations=translations[lang])

@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = request.args.get('lang', 'en')
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            
            # Debug: Check if form data is received
            print(f"Login attempt - Email: {email}, Password: {'*' * len(password)}")
            
            user = users.find_one({'email': email, 'password': password})
            
            if user:
                session['user_id'] = str(user['_id'])
                session['user_type'] = user['user_type']
                session['lang'] = lang
                
                if user['user_type'] == 'farmer':
                    return redirect(url_for('farmer_dashboard', lang=lang))
                else:
                    return redirect(url_for('school_dashboard', lang=lang))
            else:
                return render_template('login.html', error='Invalid email or password', lang=lang, translations=translations[lang])
                
        except Exception as e:
            print(f"Login error: {str(e)}")
            return render_template('login.html', error=f'Login failed: {str(e)}', lang=lang, translations=translations[lang])
    
    if lang not in translations:
        lang = 'en'
    return render_template('login.html', lang=lang, translations=translations[lang])

@app.route('/register', methods=['GET', 'POST'])
def register():
    lang = request.args.get('lang', 'en')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        district = request.form['district']
        location = request.form['location']
        
        if users.find_one({'email': email}):
            return render_template('register.html', error='Email already exists', lang=lang, translations=translations[lang])
        
        user_id = users.insert_one({
            'name': name,
            'email': email,
            'password': password,
            'user_type': user_type,
            'district': district,
            'location': location,
            'created_at': datetime.now()
        }).inserted_id
        
        session['user_id'] = str(user_id)
        session['user_type'] = user_type
        session['lang'] = lang
        
        if user_type == 'farmer':
            return redirect(url_for('farmer_dashboard', lang=lang))
        else:
            return redirect(url_for('school_dashboard', lang=lang))
    
    if lang not in translations:
        lang = 'en'
    return render_template('register.html', lang=lang, translations=translations[lang])

@app.route('/farmer_dashboard')
def farmer_dashboard():
    if 'user_id' not in session or session['user_type'] != 'farmer':
        return redirect(url_for('login'))
    
    lang = request.args.get('lang', session.get('lang', 'en'))
    if lang not in translations:
        lang = 'en'
    session['lang'] = lang
    
    farmer_id = session['user_id']
    user = users.find_one({'_id': ObjectId(farmer_id)})
    farmer_products = list(products.find({'farmer_id': farmer_id}))
    farmer_orders = list(orders.find({'farmer_id': farmer_id}))
    
    # Get nearby schools in same district
    nearby_schools = []
    if user and 'district' in user:
        nearby_schools = list(users.find({
            'user_type': 'school',
            'district': user['district']
        }))
    
    # Enrich orders with product names and calculate delivered count
    delivered_count = 0
    for order in farmer_orders:
        product = products.find_one({'_id': ObjectId(order['product_id'])})
        if product:
            order['product_name'] = product['name']
        else:
            order['product_name'] = "Unknown Product"
        
        if order['status'] == 'Delivered':
            delivered_count += 1
    
    return render_template('farmer_dashboard.html', 
                          user=user,
                          products=farmer_products,
                          farmer_products=farmer_products, 
                          orders=farmer_orders,
                          nearby_schools=nearby_schools,
                          delivered_count=delivered_count,
                          lang=lang,
                          translations=translations[lang])

@app.route('/school_dashboard')
def school_dashboard():
    if 'user_id' not in session or session['user_type'] != 'school':
        return redirect(url_for('login'))
    
    lang = request.args.get('lang', session.get('lang', 'en'))
    if lang not in translations:
        lang = 'en'
    session['lang'] = lang
    
    school_id = session['user_id']
    user = users.find_one({'_id': ObjectId(school_id)})
    
    # Get products only from farmers in the same district
    district_products = []
    if user and 'district' in user:
        # Get farmers in same district
        district_farmers = list(users.find({
            'user_type': 'farmer',
            'district': user['district']
        }))
        
        # Get farmer IDs
        farmer_ids = [str(farmer['_id']) for farmer in district_farmers]
        
        # Get products from these farmers only
        if farmer_ids:
            district_products = list(products.find({'farmer_id': {'$in': farmer_ids}}))
    
    school_orders = list(orders.find({'school_id': school_id}))
    
    # Get nearby farmers in same district
    nearby_farmers = []
    if user and 'district' in user:
        nearby_farmers = list(users.find({
            'user_type': 'farmer',
            'district': user['district']
        }))
        
        # Add product count for each farmer
        for farmer in nearby_farmers:
            farmer_id = str(farmer['_id'])
            product_count = products.count_documents({'farmer_id': farmer_id})
            farmer['products_count'] = product_count
    
    # Enrich orders with product names
    for order in school_orders:
        product = products.find_one({'_id': ObjectId(order['product_id'])})
        if product:
            order['product_name'] = product['name']
        else:
            order['product_name'] = "Unknown Product"
    
    return render_template('school_dashboard.html', 
                          user=user,
                          products=district_products, 
                          orders=school_orders,
                          nearby_farmers=nearby_farmers,
                          lang=lang,
                          translations=translations[lang])

@app.route('/messages')
def chat_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user_type = session['user_type']
    
    # Get all conversations for this user
    conversations = []
    user_messages = list(message_collection.find({
        '$or': [
            {'sender_id': user_id},
            {'recipient_id': user_id}
        ]
    }).sort('created_at', -1))
    
    # Group messages by conversation partner
    conv_dict = {}
    for msg in user_messages:
        other_user_id = msg['recipient_id'] if msg['sender_id'] == user_id else msg['sender_id']
        
        if other_user_id not in conv_dict:
            # Get other user details
            other_user = users.find_one({'_id': ObjectId(other_user_id)})
            if other_user:
                conv_dict[other_user_id] = {
                    'other_user_id': other_user_id,
                    'other_user_name': other_user['name'],
                    'last_message': msg['message'],
                    'last_message_time': msg['created_at'],
                    'unread_count': 0
                }
        
        # Count unread messages and update last message if this is more recent
        if msg['recipient_id'] == user_id and not msg.get('read', False):
            conv_dict[other_user_id]['unread_count'] += 1
        
        # Always update to most recent message
        if other_user_id in conv_dict and msg['created_at'] > conv_dict[other_user_id]['last_message_time']:
            conv_dict[other_user_id]['last_message'] = msg['message']
            conv_dict[other_user_id]['last_message_time'] = msg['created_at']
    
    conversations = list(conv_dict.values())
    conversations.sort(key=lambda x: x['last_message_time'], reverse=True)
    
    # Calculate total unread messages for notification
    total_unread = sum(conv['unread_count'] for conv in conversations)
    
    return render_template('chat_list.html', conversations=conversations, user_type=user_type, total_unread=total_unread)

@app.route('/chat/<other_user_id>')
def chat_room(other_user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    current_user_id = session['user_id']
    
    # Get other user details
    other_user = users.find_one({'_id': ObjectId(other_user_id)})
    if not other_user:
        return redirect(url_for('chat_list'))
    
    # Get chat messages between these two users
    chat_messages = list(message_collection.find({
        '$or': [
            {'sender_id': current_user_id, 'recipient_id': other_user_id},
            {'sender_id': other_user_id, 'recipient_id': current_user_id}
        ]
    }).sort('created_at', 1))
    
    # Mark messages as read
    message_collection.update_many(
        {'sender_id': other_user_id, 'recipient_id': current_user_id, 'read': {'$ne': True}},
        {'$set': {'read': True}}
    )
    
    return render_template('chat_room.html', 
                         other_user=other_user, 
                         chat_messages=chat_messages,
                         current_user_id=current_user_id)

@app.route('/send_chat_message', methods=['POST'])
def send_chat_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    recipient_id = request.form.get('recipient_id')
    message_text = request.form.get('message')
    
    if not recipient_id or not message_text:
        return redirect(url_for('chat_list'))
    
    # Get current user details
    current_user = users.find_one({'_id': ObjectId(session['user_id'])})
    recipient = users.find_one({'_id': ObjectId(recipient_id)})
    
    if not current_user or not recipient:
        return redirect(url_for('chat_list'))
    
    # Save message to database
    message_collection.insert_one({
        'sender_id': session['user_id'],
        'sender_type': session['user_type'],
        'recipient_id': recipient_id,
        'recipient_type': recipient['user_type'],
        'message': message_text,
        'sender_name': current_user['name'],
        'sender_email': current_user['email'],
        'created_at': datetime.now(),
        'read': False
    })
    
    return redirect(url_for('chat_room', other_user_id=recipient_id))

@app.route('/messages')
def messages():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        lang = request.args.get('lang', 'en')
        farmer_id = request.args.get('farmer_id')  # Get farmer_id from URL parameter
        user_id = session['user_id']
        user_type = session['user_type']
        
        # If farmer_id is provided, get farmer details for chat
        selected_farmer = None
        if farmer_id:
            try:
                selected_farmer = users.find_one({'_id': ObjectId(farmer_id), 'user_type': 'farmer'})
            except:
                pass
        
        # Get all messages for this user
        user_messages = list(message_collection.find({
            '$or': [
                {'sender_id': user_id},
                {'recipient_id': user_id}
            ]
        }).sort('created_at', -1))
        
        # Process each message
        for message in user_messages:
            if message.get('sender_id') == user_id:
                # User sent this message
                message['is_sent'] = True
                # For sent messages, get recipient info
                try:
                    recipient = users.find_one({'_id': ObjectId(message.get('recipient_id'))})
                    message['other_party_name'] = recipient.get('name', 'Unknown') if recipient else 'Unknown'
                    message['other_party_email'] = recipient.get('email', 'Unknown') if recipient else 'Unknown'
                except:
                    message['other_party_name'] = 'Unknown'
                    message['other_party_email'] = 'Unknown'
            else:
                # User received this message
                message['is_sent'] = False
                message['other_party_name'] = message.get('sender_name', 'Unknown')
                message['other_party_email'] = message.get('sender_email', 'Unknown')
        
        return render_template('messages.html', 
                             messages=user_messages, 
                             user_type=user_type, 
                             selected_farmer=selected_farmer,
                             lang=lang, 
                             translations=translations.get(lang, translations['en']))
    except Exception as e:
        return render_template('messages.html', 
                             messages=[], 
                             user_type=session.get('user_type', 'farmer'), 
                             lang='en', 
                             translations=translations['en'])

@app.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    lang = request.args.get('lang', session.get('lang', 'en'))
    if lang not in translations:
        lang = 'en'
    
    user_id = session['user_id']
    user_type = session['user_type']
    
    analytics_data = {}
    
    if user_type == 'farmer':
        # Farmer analytics
        farmer_orders = list(orders.find({'farmer_id': user_id}))
        total_revenue = sum(order['total_price'] for order in farmer_orders)
        total_orders = len(farmer_orders)
        delivered_orders = len([o for o in farmer_orders if o['status'] == 'Delivered'])
        
        # Enrich recent orders with product names
        recent_orders = farmer_orders[-5:] if farmer_orders else []
        for order in recent_orders:
            product = products.find_one({'_id': ObjectId(order['product_id'])})
            order['product_name'] = product['name'] if product else 'Unknown Product'
        
        analytics_data = {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'delivered_orders': delivered_orders,
            'pending_orders': total_orders - delivered_orders,
            'recent_orders': recent_orders
        }
    else:
        # School analytics
        school_orders = list(orders.find({'school_id': user_id}))
        total_spent = sum(order['total_price'] for order in school_orders)
        total_orders = len(school_orders)
        delivered_orders = len([o for o in school_orders if o['status'] == 'Delivered'])
        
        # Enrich recent orders with product names
        recent_orders = school_orders[-5:] if school_orders else []
        for order in recent_orders:
            product = products.find_one({'_id': ObjectId(order['product_id'])})
            order['product_name'] = product['name'] if product else 'Unknown Product'
        
        analytics_data = {
            'total_spent': total_spent,
            'total_orders': total_orders,
            'delivered_orders': delivered_orders,
            'pending_orders': total_orders - delivered_orders,
            'recent_orders': recent_orders
        }
    
    return render_template('analytics.html', analytics=analytics_data, user_type=user_type, lang=lang)

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message_text = request.form['message']
        
        try:
            # Store message in database
            contact_message = {
                'name': name,
                'email': email,
                'message': message_text,
                'created_at': datetime.now(),
                'status': 'new'
            }
            message_collection.insert_one(contact_message)
            
            # Send Telegram notification
            try:
                import requests
                telegram_bot_token = "YOUR_BOT_TOKEN_HERE"  # Replace with your bot token
                telegram_chat_id = "YOUR_CHAT_ID_HERE"     # Replace with your chat ID
                
                message = f"🔔 *New Contact Message*\n\n👤 *Name:* {name}\n📧 *Email:* {email}\n💬 *Message:* {message_text}\n⏰ *Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
                data = {
                    "chat_id": telegram_chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                }
                requests.post(url, data=data, timeout=5)
            except:
                pass  # Continue if Telegram fails
            
            # Fallback: Log to console and file
            log_message = f"\n=== NEW CONTACT MESSAGE ===\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nName: {name}\nEmail: {email}\nMessage: {message_text}\n========================\n"
            print(log_message)
            
            with open('contact_messages.txt', 'a', encoding='utf-8') as f:
                f.write(log_message)
            
            return redirect(url_for('home') + '?contact=success')
            
        except Exception as e:
            # Still save to database even if email fails
            try:
                contact_message = {
                    'name': name,
                    'email': email,
                    'message': message_text,
                    'created_at': datetime.now(),
                    'status': 'new'
                }
                message_collection.insert_one(contact_message)
                return redirect(url_for('home') + '?contact=success')
            except:
                return redirect(url_for('home') + '?contact=error')
    
    return redirect(url_for('home'))

@app.route('/add_product', methods=['POST'])
def add_product():
    if 'user_id' not in session or session['user_type'] != 'farmer':
        return redirect(url_for('login'))
    
    name = request.form['name'].lower()
    description = request.form['description']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    category = request.form['category']
    
    # Determine unit based on product name
    litre_products = ['milk', 'buttermilk', 'lassi', 'coconut milk', 'almond milk', 'soy milk', 'juice', 'oil', 'vinegar', 'honey', 'water', 'syrup', 'sauce']
    gram_products = ['paneer', 'cheese', 'butter', 'ghee', 'cream cheese', 'cottage cheese', 'mozzarella', 'cheddar', 'spices', 'salt', 'sugar', 'jaggery', 'turmeric', 'chili powder', 'cumin', 'coriander', 'garam masala', 'black pepper', 'cardamom', 'cinnamon', 'cloves', 'nutmeg', 'saffron', 'tea', 'coffee', 'nuts', 'almonds', 'cashews', 'pistachios', 'walnuts', 'peanuts', 'raisins', 'dates', 'figs']
    dozen_products = ['egg', 'eggs', 'banana', 'bananas', 'orange', 'oranges', 'apple', 'apples', 'mango', 'mangoes', 'coconut', 'coconuts']
    piece_products = ['pumpkin', 'watermelon', 'jackfruit', 'cauliflower', 'cabbage', 'lettuce', 'broccoli', 'corn', 'pineapple']
    bundle_products = ['spinach', 'coriander', 'mint', 'fenugreek', 'dill', 'curry leaves', 'green onion', 'spring onion']
    
    if any(liquid in name for liquid in litre_products):
        unit = 'litres'
    elif any(gram_prod in name for gram_prod in gram_products):
        unit = 'grams'
    elif any(dozen_prod in name for dozen_prod in dozen_products):
        unit = 'dozens'
    elif any(piece_prod in name for piece_prod in piece_products):
        unit = 'pieces'
    elif any(bundle_prod in name for bundle_prod in bundle_products):
        unit = 'bundles'
    else:
        unit = 'kgs'
    
    products.insert_one({
        'farmer_id': session['user_id'],
        'name': request.form['name'],  # Store original case
        'description': description,
        'price': price,
        'quantity': quantity,
        'category': category,
        'unit': unit,
        'created_at': datetime.now()
    })
    
    return redirect(url_for('farmer_dashboard'))

@app.route('/delete_product', methods=['POST'])
def delete_product():
    if 'user_id' not in session or session['user_type'] != 'farmer':
        return redirect(url_for('login'))
    
    product_id = request.form['product_id']
    products.delete_one({'_id': ObjectId(product_id), 'farmer_id': session['user_id']})
    
    return redirect(url_for('farmer_dashboard'))

@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    if 'user_id' not in session or session['user_type'] != 'farmer':
        return redirect(url_for('login'))
    
    order_id = request.form['order_id']
    status = request.form['status']
    
    orders.update_one(
        {'_id': ObjectId(order_id), 'farmer_id': session['user_id']},
        {'$set': {'status': status, 'updated_at': datetime.now()}}
    )
    
    return redirect(url_for('farmer_dashboard'))

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session or session['user_type'] != 'school':
        return redirect(url_for('login'))
    
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    
    product = products.find_one({'_id': ObjectId(product_id)})
    if not product or product['quantity'] < quantity:
        return redirect(url_for('school_dashboard'))
    
    total_price = product['price'] * quantity
    
    orders.insert_one({
        'school_id': session['user_id'],
        'farmer_id': product['farmer_id'],
        'product_id': product_id,
        'quantity': quantity,
        'total_price': total_price,
        'status': 'Pending',
        'created_at': datetime.now()
    })
    
    # Update product quantity
    products.update_one(
        {'_id': ObjectId(product_id)},
        {'$inc': {'quantity': -quantity}}
    )
    
    return redirect(url_for('school_dashboard'))

@app.route('/contact_farmer/<farmer_id>')
def contact_farmer(farmer_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        farmer = users.find_one({'_id': ObjectId(farmer_id), 'user_type': 'farmer'})
        if not farmer:
            return redirect(url_for('school_dashboard'))
        
        # Get farmer's products
        farmer_products = list(products.find({'farmer_id': farmer_id}))
        
        return render_template('contact_farmer.html', farmer=farmer, products=farmer_products)
    except Exception as e:
        return redirect(url_for('school_dashboard'))

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        recipient_id = request.form.get('farmer_id') or request.form.get('recipient_id')
        message_text = request.form.get('message', '')
        form_sender_name = request.form.get('sender_name', '')
        form_sender_email = request.form.get('sender_email', '')
        
        if not recipient_id or not message_text:
            return redirect(url_for('messages'))
        
        # Get current user details
        current_user = users.find_one({'_id': ObjectId(session['user_id'])})
        recipient = users.find_one({'_id': ObjectId(recipient_id)})
        
        if not current_user or not recipient:
            return redirect(url_for('messages'))
        
        # Use form data if provided, otherwise use current user data
        sender_name = form_sender_name if form_sender_name else current_user.get('name', 'Unknown')
        sender_email = form_sender_email if form_sender_email else current_user.get('email', 'Unknown')
        
        # Save message to database
        message_collection.insert_one({
            'sender_id': session['user_id'],
            'sender_type': session['user_type'],
            'recipient_id': recipient_id,
            'recipient_type': recipient.get('user_type', 'farmer'),
            'message': message_text,
            'sender_name': sender_name,
            'sender_email': sender_email,
            'created_at': datetime.now(),
            'read': False
        })
        
        # Redirect back to messages with farmer_id if it was provided
        if session['user_type'] == 'school' and request.form.get('recipient_id'):
            return redirect(url_for('messages', farmer_id=recipient_id) + '&sent=1')
        elif session['user_type'] == 'school':
            return redirect(url_for('contact_farmer', farmer_id=recipient_id) + '?sent=1')
        else:
            return redirect(url_for('messages') + '?sent=1')
    except Exception as e:
        return redirect(url_for('messages'))

@app.route('/send_quick_message', methods=['POST'])
def send_quick_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    message_text = request.form.get('message', '')
    if not message_text:
        return redirect(url_for('messages'))
    
    # For now, just redirect back - this would need recipient selection
    return redirect(url_for('messages') + '?sent=1')

@app.route('/reply_message', methods=['POST'])
def reply_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        recipient_id = request.form.get('recipient_id')
        message_text = request.form.get('message')
        
        if not recipient_id or not message_text:
            return redirect(url_for('messages'))
        
        # Get current user details
        current_user = users.find_one({'_id': ObjectId(session['user_id'])})
        recipient = users.find_one({'_id': ObjectId(recipient_id)})
        
        if not current_user or not recipient:
            return redirect(url_for('messages'))
        
        # Save reply to database
        message_collection.insert_one({
            'sender_id': session['user_id'],
            'sender_type': session['user_type'],
            'recipient_id': recipient_id,
            'recipient_type': recipient['user_type'],
            'message': message_text,
            'sender_name': current_user['name'],
            'sender_email': current_user['email'],
            'created_at': datetime.now(),
            'read': False
        })
        
        return redirect(url_for('messages') + '?sent=1')
    except Exception as e:
        return redirect(url_for('messages'))

@app.route('/upload_media', methods=['POST'])
def upload_media():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'media' not in request.files:
        return 'No file', 400
    
    file = request.files['media']
    recipient_id = request.form.get('recipient_id')
    
    if file.filename == '':
        return 'No file selected', 400
    
    # Create uploads directory if it doesn't exist
    import os
    upload_dir = 'static/uploads'
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file with unique name
    from werkzeug.utils import secure_filename
    import uuid
    filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)
    
    # Determine media type
    media_type = 'image' if file.content_type.startswith('image/') else 'video'
    
    # Get current user details
    current_user = users.find_one({'_id': ObjectId(session['user_id'])})
    recipient = users.find_one({'_id': ObjectId(recipient_id)})
    
    # Save message with media
    message_collection.insert_one({
        'sender_id': session['user_id'],
        'sender_type': session['user_type'],
        'recipient_id': recipient_id,
        'recipient_type': recipient['user_type'],
        'message': f'Sent a {media_type}',
        'media_type': media_type,
        'media_url': '/' + file_path.replace('\\', '/'),
        'sender_name': current_user['name'],
        'sender_email': current_user['email'],
        'created_at': datetime.now(),
        'read': False
    })
    
    return 'OK'

@app.route('/edit_message', methods=['POST'])
def edit_message():
    if 'user_id' not in session:
        return 'Unauthorized', 401
    
    data = request.get_json()
    message_id = data.get('message_id')
    new_text = data.get('new_text')
    
    # Update message if user owns it
    result = message_collection.update_one(
        {'_id': ObjectId(message_id), 'sender_id': session['user_id']},
        {'$set': {'message': new_text, 'edited': True}}
    )
    
    return 'OK' if result.modified_count > 0 else 'Failed', 400

@app.route('/delete_message', methods=['POST'])
def delete_message():
    if 'user_id' not in session:
        return 'Unauthorized', 401
    
    data = request.get_json()
    message_id = data.get('message_id')
    
    # Mark message as deleted if user owns it
    result = message_collection.update_one(
        {'_id': ObjectId(message_id), 'sender_id': session['user_id']},
        {'$set': {'deleted': True, 'message': 'This message was deleted'}}
    )
    
    return 'OK' if result.modified_count > 0 else 'Failed', 400

@app.route('/api/unread_count')
def get_unread_count():
    if 'user_id' not in session:
        return {'unread_count': 0}
    
    user_id = session['user_id']
    unread_count = message_collection.count_documents({
        'recipient_id': user_id,
        'read': {'$ne': True}
    })
    
    return {'unread_count': unread_count}

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)