# Farm2School Platform 🌾

A comprehensive farm-to-school platform connecting local farmers with educational institutions for fresh, sustainable food supply.

## Features ✨

### 🚀 Core Functionality
- **User Authentication** - Separate login/register for farmers and schools
- **District-Based Matching** - Location-based farmer-school connections
- **Product Management** - Smart unit detection (kgs/litres/dozens/pieces/bundles)
- **Order Management** - Complete order lifecycle with status tracking
- **Real-Time Chat** - WhatsApp-style messaging with media support
- **Analytics Dashboard** - Revenue and order tracking

### 💬 Advanced Chat Features
- **Message Editing & Deletion** - Fix typos and remove mistakes
- **Media Sharing** - Upload images and videos
- **Read Receipts** - Blue tick system like WhatsApp
- **Real-Time Notifications** - Instant message alerts
- **Message History** - Persistent chat storage

### 🌍 Multilingual Support
- **3 Languages** - English, Tamil (தமிழ்), Hindi (हिं)
- **Complete Translation** - All pages and features
- **Language Switcher** - Easy language selection

### 📱 Modern UI/UX
- **Responsive Design** - Works on all devices
- **Beautiful Backgrounds** - Themed images for each section
- **Animated Elements** - Smooth transitions and effects
- **Professional Styling** - Clean, modern interface

## Tech Stack 🛠️

- **Backend**: Python Flask
- **Database**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with gradients and animations
- **Icons**: Font Awesome
- **Notifications**: Telegram Bot API

## Installation & Setup 📦

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Farm2School
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MongoDB**
   - Install MongoDB locally
   - Start MongoDB service
   - Database will be created automatically

4. **Configure Telegram Bot (Optional)**
   - Create bot via @BotFather on Telegram
   - Update bot token and chat ID in app.py

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the platform**
   - Open browser to `http://localhost:5000`
   - Select language and start using!

## Project Structure 📁

```
Farm2School/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── script.js     # JavaScript functionality
│   ├── images/           # Logo and images
│   └── uploads/          # User uploaded media
└── templates/
    ├── language_select.html      # Language selection page
    ├── index_multilingual.html   # Home page
    ├── login.html               # Login page
    ├── register.html            # Registration page
    ├── farmer_dashboard.html    # Farmer dashboard
    ├── school_dashboard.html    # School dashboard
    ├── chat_list.html          # Chat conversations list
    ├── chat_room.html          # Individual chat interface
    ├── analytics.html          # Analytics dashboard
    └── messages.html           # Legacy messages (backup)
```

## Key Features Explained 🔍

### Smart Unit Detection
Products automatically get appropriate units:
- **Litres**: milk, juice, oil, honey
- **Dozens**: eggs, bananas, apples, oranges
- **Pieces**: pumpkin, watermelon, cauliflower
- **Bundles**: spinach, coriander, mint
- **Grams**: paneer, spices, nuts, tea
- **Kgs**: everything else (default)

### District-Based System
- Farmers only see schools in their district
- Schools only see farmers in their district
- Promotes local food systems
- Reduces transportation costs

### Real-Time Chat System
- WhatsApp-style interface
- Message editing and deletion
- Media sharing (images/videos)
- Read receipts with blue ticks
- Notification badges
- Message history preservation

### Multilingual Support
Complete translation system supporting:
- **English** - Default language
- **Tamil** - தமிழ் (Regional language)
- **Hindi** - हिंदी (National language)

## Usage Guide 👥

### For Farmers 🚜
1. Register as a farmer with district info
2. Add products with automatic unit detection
3. Manage orders and update status
4. Chat with schools in your district
5. View analytics and revenue data

### For Schools 🏫
1. Register as a school with district info
2. Browse local farmers and products
3. Place orders for fresh produce
4. Chat with farmers for coordination
5. Track order status and history

## Contributing 🤝

This is a complete, production-ready platform. For enhancements:
1. Fork the repository
2. Create feature branch
3. Make improvements
4. Submit pull request

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For support or questions:
- Check the code documentation
- Review the feature implementations
- Contact the development team

---

**Farm2School** - *Connecting Farms to Schools for a Healthier Future* 🌱