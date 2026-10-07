# 🧞‍♂️ CSE 15 Akinator

> **Interactive Heuristic Akinator Game for ABES Engineering College • CSE-15 (Batch 2025–2029)**  
> Built with HTML5, CSS3, Vanilla JavaScript, and Cryptographic Security.

---

## 🎯 About The Project
**CSE 15 Akinator** is an AI-inspired guessing game tailored specifically for the 80 students of Department of Computer Science & Engineering, Section CSE-15. 

Think of any classmate in the batch, answer up to 5 sequential questions, and the student genie will accurately guess who you're thinking of!

---

## ⚡ Heuristic Filtering Sequence
The game narrows down 80 candidates using 5 sequential questions:
1. **Gender:** Male or Female?
2. **First Letter:** First letter of their name (`A`, `B`, `C`, `D`).
3. **Word Count:** Words in their name (`1 Word`, `2 Words`, `3 Words`) — *(e.g., Arvind Kumar = 2 words)*.
4. **Roll Last Digit:** Last digit of their university roll number (`0` to `9`).
5. **Previous Section:** Their previous section before transferring to CSE-15 (`CSE11` to `CSE20`).
6. **Tie-Breaker:** 2nd letter of first name (only needed for 4 specific identical attribute pairs).

**Success Rate:** **72 / 80 (90%)** identified by Question 5, and **100% (80/80)** identified with the single tie-breaker.

---

## 🔒 Security & Student Privacy
To prevent scraping or unauthorized extraction via Chrome DevTools (`F12` / Inspect Element):
* **Cryptographic Data Protection:** All student phone numbers in `students.json` are encrypted using XOR stream cipher keyed to a master SHA-256 hash. Zero plain-text numbers exist in client-side code.
* **1-Day Expiring Developer Keys:** Contact numbers require an access key that rotates daily.
* **Anti-Inspect Shield:** Disables right-click and inspection shortcuts.

---

## 🔑 How to Generate Today's Access Key (For Developer)
To post today's active key in the Telegram channel:
```bash
python generate_key.py
```
This prints the unique daily key (e.g., `CSE15-OCT07-968FB`) that expires at midnight (23:59:59).

---

## 🚀 How to Run Locally
Simply open `index.html` in any web browser, or serve it with Python:
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000` in your browser.

---

## 🌐 Deploy to GitHub Pages (Free Hosting)
1. Commit and push this directory to your repository:
   ```bash
   git add .
   git commit -m "Launch CSE 15 Akinator"
   git push origin main
   ```
2. In your GitHub repo: **Settings** $\rightarrow$ **Pages** $\rightarrow$ Branch: `main` / `root` $\rightarrow$ **Save**.
3. Your game is live worldwide at:  
   👉 `https://arvindkumar298.github.io/Mini-Project/`

---

## 👨‍💻 Developer & Credits
* **Developer:** **Arvind Kumar**
* **Roll Number:** 2503201000298
* **College:** ABES Engineering College, Ghaziabad
* **Telegram Channel:** [CSE-15 Akinator Access Channel](https://t.me/+SNXgNiPCwMAxMjdl)
* **GitHub:** [@ArvindKumar298](https://github.com/ArvindKumar298/Mini-Project)
* **LinkedIn:** [Arvind Kumar](https://www.linkedin.com/in/arvind-kumar-635747375)
