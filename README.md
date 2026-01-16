 ♻️ Trash-Sorter AI: Intelligent Waste Classification

Trash-Sorter AI is a full-stack Computer Vision application designed to solve the common problem of "wish-cycling" (recycling things that don't belong in the bin). By leveraging Deep Learning, it identifies household waste and directs users to the correct disposal bin.

 🧠 The Brain: ResNet-34
For this project, I chose the ResNet-34 (Residual Network) architecture. 
- Why? Unlike standard CNNs, ResNet uses "skip connections" to avoid the vanishing gradient problem.
- Strength: It is particularly effective at recognizing material textures (like the difference between a metallic soda can and a plastic water bottle).

 🚀 Features
- Real-time Identification: Instant classification of objects like bottles, cans, and paper.
- Sorting Logic: Custom mapping that translates ImageNet labels into localized recycling bin rules.
- Modern UI: A clean, eco-friendly web interface built with FastAPI and Jinja2.

 🛠️ Tech Stack
- AI Framework: PyTorch & Torchvision
- Backend: FastAPI (Python)
- Frontend: HTML5, CSS3, Jinja2
- Infrastructure: Uvicorn (ASGI server)

 📦 How to Run
1. Clone the repo: `git clone https://github.com/Dipanshu-Chaubey3/trash-sorter-ai.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the app: `uvicorn src.app:app --reload`
4. Access at: `http://127.0.0.1:8000`
