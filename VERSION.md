# Version History

## v2.1.0 (2025-11-05)
**Gemini 2.5 Model Upgrade**

### 🔧 Fixed
- Fixed 404 error with deprecated Gemini models
- Updated from `gemini-pro` to `gemini-2.5-flash`
- Gemini 1.0 and 1.5 models are retired as of 2025

### 📝 Technical Details
- **Old Model:** `gemini-pro` (deprecated)
- **New Model:** `gemini-2.5-flash` (current)
- **API Version:** v1beta
- **Reason:** Google retired Gemini 1.x models, all users must migrate to 2.x

### 🔗 References
- [Gemini API Models Documentation](https://ai.google.dev/gemini-api/docs/models)
- Gemini 2.5 series offers improved performance and accuracy
- Free tier remains: 60 requests/minute, 128K tokens/minute

---

## v2.0.0 (2025-11-05)
**AI Recipe Generator with Google Gemini**

### ✨ Added
- Integrated Google Gemini AI for intelligent recipe generation
- Smart prompt engineering for realistic, cookable recipes
- Comprehensive error handling with helpful messages
- README.md with complete setup instructions
- API key configuration via environment variable

### 🔧 Changed
- Replaced template-based system with real AI
- No more nonsensical ingredient combinations
- Recipes now intelligently match available ingredients

### 📦 Dependencies
- Added `google-generativeai>=0.3.0`
- Updated `requirements.txt`

### 🎯 Features
- Analyzes fridge ingredients
- Generates sensible, cookable recipes
- JSON-formatted responses
- Markdown cleanup for clean parsing
- Fallback logic when API key missing

---

## v1.1.0 (2025-11-05)
**Initial AI Recipe Button**

### ✨ Added
- Orange gradient "🤖 KI Rezept" button next to search bar
- Beautiful modal UI for recipe display
- Template-based recipe generation system
- Ingredient categorization (vegetables, meat, dairy, carbs, etc.)
- Multiple recipe templates (pasta, salad, pan dishes, omelette, soup)

### 🎨 UI Improvements
- Responsive modal design
- Ingredient list with styling
- Step-by-step preparation instructions
- Cooking time and serving size display

---

## v1.0.0 (Initial Release)
**Coolio - Smart Fridge App**

### ✨ Features
- Progressive Web App (PWA) support
- Barcode scanner with camera integration
- OpenFoodFacts API integration
- Multi-user support with authentication
- Product expiry date tracking
- Live search functionality
- Admin panel for user management

### 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** Vanilla JavaScript + HTML
- **Database:** JSON file storage
- **APIs:** OpenFoodFacts for product lookup

---

## Model Version Information

### Current AI Model
- **Model:** `gemini-2.5-flash`
- **Provider:** Google AI (Gemini API)
- **API Version:** v1beta
- **Cost:** Free (60 req/min, 128K tokens/min)
- **Date:** 2025-11-05

### Previous Models (Deprecated)
- ~~`gemini-1.5-flash`~~ - Retired 2025
- ~~`gemini-pro`~~ - Retired 2025
- ~~`gemini-1.0-pro`~~ - Retired 2025

### Migration Notes
If you encounter 404 errors with Gemini models:
1. Ensure you're using `gemini-2.5-flash` or `gemini-2.5-pro`
2. Update `google-generativeai` to latest version: `pip install --upgrade google-generativeai`
3. Check [Google AI Studio](https://ai.google.dev/gemini-api/docs/models) for current model availability

---

## Compatibility

### Python Version
- **Required:** Python 3.9+
- **Tested:** Python 3.11

### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### API Dependencies
- Google Gemini API (Free tier)
- OpenFoodFacts API (Free, no key required)

---

## Roadmap

### Upcoming Features (v2.2.0)
- [ ] Export recipes as PDF
- [ ] Shopping list generator
- [ ] Nutrition facts tracking
- [ ] Save favorite recipes
- [ ] Recipe rating system
- [ ] Multi-language support

### Future Considerations
- [ ] Mobile app (React Native)
- [ ] Image recognition for ingredients
- [ ] Meal planning calendar
- [ ] Integration with smart home devices

---

**Maintained by:** Coolio Development Team
**License:** MIT
**Last Updated:** 2025-11-05
