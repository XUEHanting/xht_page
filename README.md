# NoteTaker - Personal Note Management Application

A modern, responsive web application for managing personal notes with a beautiful user interface and full CRUD functionality.

## 🌟 Features

- **Create Notes**: Add new notes with titles and rich content
- **Edit Notes**: Update existing notes with real-time editing
- **Delete Notes**: Remove notes you no longer need
- **Search Notes**: Find notes quickly by searching titles and content
- **Auto-save**: Notes are automatically saved as you type
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Updates**: Instant feedback and updates
- **Translate Notes**: Translate note content to Chinese or English via OpenRouter

## 🚀 Live Demo

The application is deployed and accessible at: **https://3dhkilc88dkk.manus.space**

## 🛠 Technology Stack

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and API communication

### Backend
- **Python Flask**: Web framework for API endpoints
- **supabase-py**: Official Supabase client for database access
- **Flask-CORS**: Cross-origin resource sharing support

### Database
- **Supabase (PostgreSQL)**: Hosted Postgres with Data API

## 📁 Project Structure

```
notetaking-app/
├── src/
│   ├── models/
│   │   ├── user.py              # Placeholder (auth not implemented)
│   │   └── note.py              # Note response helpers
│   ├── routes/
│   │   ├── user.py              # User API placeholder
│   │   └── note.py              # Note API endpoints (Supabase)
│   ├── services/
│   │   ├── supabase_client.py   # Supabase client factory
│   │   └── translator.py        # OpenRouter translation service
│   ├── static/
│   │   ├── index.html           # Frontend application
│   │   └── favicon.ico          # Application icon
│   └── main.py                  # Flask application entry point
├── supabase/
│   └── schema.sql               # SQL to create the notes table
├── .env.example                 # Example environment variables
├── venv/                        # Python virtual environment
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- A [Supabase](https://supabase.com/) project

### Installation Steps

1. **Create / activate the virtual environment**
   ```bash
   python -m venv venv
   ```

   ```bash
   source venv/bin/activate
   ```

   Remark: On Windows, use `venv\Scripts\activate`

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create the Supabase table**
   - Open your Supabase project → **SQL Editor**
   - Paste and run the contents of `supabase/schema.sql`

4. **Configure environment variables**
   ```bash
   copy .env.example .env
   ```
   Then edit `.env` and set:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY` (Project Settings → API → `service_role`)
   - `OPENROUTER_API_KEY` (optional, only needed for translation)

5. **Run the application**
   ```bash
   python src/main.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:5001`

## 📡 API Endpoints

### Notes API
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create a new note
- `GET /api/notes/<id>` - Get a specific note
- `PUT /api/notes/<id>` - Update a note
- `DELETE /api/notes/<id>` - Delete a note
- `GET /api/notes/search?q=<query>` - Search notes
- `POST /api/notes/translate` - Translate note title and content (`title`, `content`, `target_lang`: `zh` or `en`)

### Request/Response Format
```json
{
  "id": 1,
  "title": "My Note Title",
  "content": "Note content here...",
  "created_at": "2025-09-03T11:26:38.123456+00:00",
  "updated_at": "2025-09-03T11:27:30.654321+00:00"
}
```

## 🎨 User Interface Features

### Sidebar
- **Search Box**: Real-time search through note titles and content
- **New Note Button**: Create new notes instantly
- **Notes List**: Scrollable list of all notes with previews
- **Note Previews**: Show title, content preview, and last modified date

### Editor Panel
- **Title Input**: Edit note titles
- **Content Textarea**: Rich text editing area
- **Translate Controls**: Choose Chinese/English and translate the current content
- **Save Button**: Manual save option (auto-save also available)
- **Delete Button**: Remove notes with confirmation
- **Real-time Updates**: Changes reflected immediately

### Design Elements
- **Gradient Background**: Beautiful purple gradient backdrop
- **Glass Morphism**: Semi-transparent panels with backdrop blur
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adapts to different screen sizes
- **Modern Typography**: Clean, readable font stack

## 🔒 Database Schema

Create the table with `supabase/schema.sql`. Equivalent structure:

```sql
create table public.notes (
  id bigint generated by default as identity primary key,
  title text not null default '',
  content text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

## 🚀 Deployment

The application is configured for easy deployment with:
- CORS enabled for cross-origin requests
- Host binding to `0.0.0.0` for external access
- Production-ready Flask configuration
- Supabase-hosted PostgreSQL for persistent storage

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `SECRET_KEY`: Flask secret key for sessions
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Supabase service role key (preferred for this backend)
- `SUPABASE_KEY`: Optional alias for the Supabase key
- `OPENROUTER_API_KEY`: OpenRouter API key used by the translate feature
- `OPENROUTER_MODEL`: Optional model override (default: `deepseek/deepseek-v4.1-flash`)

### Database Configuration
- Provider: Supabase PostgreSQL
- Access: `supabase-py` Data API from the Flask backend
- Schema file: `supabase/schema.sql`

## 📱 Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the browser console for error messages
2. Verify the Flask server is running
3. Ensure Supabase credentials are set in `.env`
4. Confirm `supabase/schema.sql` was executed in your project
5. Ensure all dependencies are installed

## 🎯 Future Enhancements

Potential improvements for future versions:
- User authentication and multi-user support (Supabase Auth + RLS)
- Note categories and tags
- Rich text formatting (bold, italic, lists)
- File attachments
- Export functionality (PDF, Markdown)
- Dark/light theme toggle
- Offline support with service workers
- Note sharing capabilities

---

**Built with ❤️ using Flask, Supabase, and modern web technologies**
