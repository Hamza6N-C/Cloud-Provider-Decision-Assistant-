***Overview***

This Streamlit application helps organizations make data-driven cloud architecture decisions by:

- Analyzing business use cases with AI

- Scoring major cloud providers across 23 critical criteria

- Generating weighted recommendations based on your priorities


***Key Features***

🧠 AI-Powered Analysis:
- Uses OpenAI's GPT-4 model to analyze your business requirements
- Generates scores for 11 cloud providers across 23 technical and business criteria
- Handles complex technical requirements and business constraints

⚖️ Custom Weighting System:
- Adjust importance of each criterion with interactive sliders
- See recommendations update in real-time
- Compare providers based on your unique priorities

📊 Visual Comparison:
- Interactive score matrix for easy comparison
- Clear ranking of providers based on weighted scores
- Exportable results for stakeholder presentations

***Getting Started***

Prerequisites:
- Python 3.8+
- OpenAI API key
- Streamlit

Installation:
# Clone repository
git clone https://github.com/yourusername/cloud-decision-assistant.git
cd cloud-decision-assistant

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Running the Application
streamlit run app.py


***Usage Guide***

# Describe Your Use Case:
Enter your business/technical requirements in the text area

# Generate Scores:
Click "Generate Scores" to get AI-powered provider evaluations

# Adjust Weights
Modify importance of each criterion using sliders

#  Get Recommendation
See your optimal cloud provider based on weighted scores

***Supported Cloud Providers***

- AWS: Amazon Web Services
- Azure:	Microsoft Azure
- GCP:	Google Cloud Platform
- Oracle:	Oracle Cloud Infrastructure
- IBM:	IBM Cloud
- Alibaba:	Alibaba Cloud
- DigitalOcean:	Developer-friendly cloud
- Linode:	Akamai's cloud computing
- Vultr:	High-performance cloud
- Hetzner:	German cloud provider
- T-Systems:	Deutsche Telekom's cloud

***Evaluation Criteria***
The application evaluates providers across 23 dimensions:
Core Infrastructure Offerings
Security Parameters
Performance (Latency/Throughput)
Service Category Coverage
Suitability for Organization
Reliability / Uptime
Enterprise Integration
AI / ML / Data Capabilities
Pricing & Flexibility
Range of Services
Quality of Services
Compliance Certifications
Developer Experience
Modern Architecture Support
Regional Strength
Hybrid/Multicloud Support
Brand Trust / Familiarity
Vendor Lock-in Risk
Ecosystem / Marketplace
Innovation Velocity
Marketing/Perception
Free Tier / Trial
Niche Services

***Future Enhancements***
Multi-use case comparison dashboard
Historical decision tracking
Cost estimation integration
Provider-specific architecture templates
Team collaboration features


Developed as part of my Master's Thesis in Cloud Architecture Decision Frameworks
