/**
 * CSE 15 AKINATOR - CORE LOGIC & ENGINE
 * Developer: Arvind Kumar (Roll No. 2503201000298)
 * ABES Engineering College, Ghaziabad
 */

const MASTER_SALT = "ARVIND_KUMAR_CSE15_SECRET_2026";
let allStudents = [];
let activePool = [];
let currentStep = 1;
let guessedStudent = null;
let isPhoneUnlocked = false;

// -------------------------------------------------------------
// Initialization
// -------------------------------------------------------------
window.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch('students.json');
    allStudents = await res.json();
    console.log(`Loaded ${allStudents.length} students securely.`);
  } catch (err) {
    console.error('Failed to load students.json:', err);
  }
  setupPrivacyShield();
});

// -------------------------------------------------------------
// Privacy & DevTools Shield
// -------------------------------------------------------------
function setupPrivacyShield() {
  document.addEventListener('contextmenu', (e) => e.preventDefault());
  document.addEventListener('keydown', (e) => {
    // F12 or Ctrl+Shift+I or Ctrl+Shift+J or Ctrl+U
    if (
      e.key === 'F12' ||
      (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'i' || e.key === 'J' || e.key === 'j')) ||
      (e.ctrlKey && (e.key === 'U' || e.key === 'u'))
    ) {
      e.preventDefault();
    }
  });
}

// -------------------------------------------------------------
// Navigation Between Screens
// -------------------------------------------------------------
function showScreen(screenId) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  const target = document.getElementById(screenId);
  if (target) {
    target.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

function startGame() {
  activePool = [...allStudents];
  currentStep = 1;
  guessedStudent = null;
  isPhoneUnlocked = false;
  showScreen('screen-question');
  renderCurrentQuestion();
}

function restartGame() {
  startGame();
}

// -------------------------------------------------------------
// Sequential Heuristic Engine
// -------------------------------------------------------------
function renderCurrentQuestion() {
  const poolBadge = document.getElementById('pool-count');
  if (poolBadge) poolBadge.innerText = activePool.length;

  // If already down to 1 student, declare victory immediately!
  if (activePool.length === 1) {
    triggerVictory(activePool[0]);
    return;
  }

  const stepLabel = document.getElementById('q-step-label');
  const qTitle = document.getElementById('q-title');
  const hintContainer = document.getElementById('q-hint-container');
  const hintText = document.getElementById('q-hint-text');
  const optionsBox = document.getElementById('options-box');

  optionsBox.innerHTML = '';
  hintContainer.style.display = 'none';

  if (currentStep === 1) {
    // Question 1: Gender
    stepLabel.innerText = "Question 1 of 5";
    qTitle.innerText = "Does the student is Male or Female?";

    const genders = [
      { key: 'M', label: '👨 Male' },
      { key: 'F', label: '👩 Female' }
    ];

    genders.forEach(g => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      btn.innerText = g.label;
      btn.onclick = () => filterSelection('gender', g.key);
      optionsBox.appendChild(btn);
    });

  } else if (currentStep === 2) {
    // Question 2: First Letter
    stepLabel.innerText = "Question 2 of 5";
    qTitle.innerText = "Which one is the first letter of their name?";

    const availableLetters = [...new Set(activePool.map(s => s.first_letter))].sort();
    availableLetters.forEach(letter => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      btn.innerText = `Letter "${letter}"`;
      btn.onclick = () => filterSelection('first_letter', letter);
      optionsBox.appendChild(btn);
    });

  } else if (currentStep === 3) {
    // Question 3: Number of words in name
    stepLabel.innerText = "Question 3 of 5";
    qTitle.innerText = "How many words are there in the student's name?";
    
    // Example hint as requested!
    hintContainer.style.display = 'inline-block';
    hintText.innerText = "(e.g., Arvind Kumar word count is 2)";

    const wordCounts = [...new Set(activePool.map(s => s.words_count))].sort((a, b) => a - b);
    wordCounts.forEach(count => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      btn.innerText = `${count} Word${count > 1 ? 's' : ''}`;
      btn.onclick = () => filterSelection('words_count', count);
      optionsBox.appendChild(btn);
    });

  } else if (currentStep === 4) {
    // Question 4: Last digit of roll number
    stepLabel.innerText = "Question 4 of 5";
    qTitle.innerText = "What is the last digit of the student's roll number?";

    const digits = [...new Set(activePool.map(s => s.roll_last))].sort((a, b) => a - b);
    digits.forEach(digit => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      btn.innerText = `Ends with ${digit}`;
      btn.onclick = () => filterSelection('roll_last', digit);
      optionsBox.appendChild(btn);
    });

  } else if (currentStep === 5) {
    // Question 5: Previous Section
    stepLabel.innerText = "Question 5 of 5";
    qTitle.innerText = "Which is their previous section?";

    const sections = [...new Set(activePool.map(s => s.prev_section))].sort();
    sections.forEach(sec => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      btn.innerText = sec;
      btn.onclick = () => filterSelection('prev_section', sec);
      optionsBox.appendChild(btn);
    });

  } else if (currentStep === 6) {
    // Tie-breaker question (Only needed for the 4 identical pairs)
    stepLabel.innerText = "Tie-Breaker Question";
    qTitle.innerText = "What is the second letter of their first name?";

    const secLetters = [...new Set(activePool.map(s => s.second_letter))].sort();
    secLetters.forEach(l => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      btn.innerText = `Letter "${l}"`;
      btn.onclick = () => filterSelection('second_letter', l);
      optionsBox.appendChild(btn);
    });
  }
}

function filterSelection(property, value) {
  activePool = activePool.filter(s => s[property] === value);

  if (activePool.length === 1) {
    triggerVictory(activePool[0]);
  } else if (activePool.length === 0) {
    alert("No student found with those exact attributes. Let's try again!");
    restartGame();
  } else {
    currentStep++;
    renderCurrentQuestion();
  }
}

// -------------------------------------------------------------
// Victory / End Screen
// -------------------------------------------------------------
function triggerVictory(student) {
  guessedStudent = student;
  isPhoneUnlocked = false;

  document.getElementById('vic-name').innerText = student.name;
  document.getElementById('vic-curr-sec').innerText = student.new_section || "CSE15";
  document.getElementById('vic-prev-sec').innerText = student.prev_section;
  document.getElementById('vic-roll').innerText = student.roll_no;
  
  // Reset phone display
  const phoneDisplay = document.getElementById('vic-phone-display');
  phoneDisplay.innerText = "+91 ••••• •••••";
  phoneDisplay.style.color = "#92400e";
  
  const unlockBtn = document.getElementById('btn-unlock-trigger');
  unlockBtn.innerText = "🔒 Unlock";
  unlockBtn.disabled = false;

  // Build WhatsApp share link
  const gameUrl = window.location.href;
  const shareText = `Akinator just guessed ${student.name} from CSE-15! Can you beat it? Play here: ${gameUrl}`;
  const waUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(shareText)}`;
  document.getElementById('btn-wa-share').href = waUrl;

  showScreen('screen-victory');
}

// -------------------------------------------------------------
// Daily Security Key Decryption
// -------------------------------------------------------------
function openKeyModal() {
  document.getElementById('daily-key-input').value = '';
  document.getElementById('key-modal').classList.add('active');
  document.getElementById('daily-key-input').focus();
}

function closeKeyModal() {
  document.getElementById('key-modal').classList.remove('active');
}

function openPicModal() {
  document.getElementById('pic-modal').classList.add('active');
}

function closePicModal() {
  document.getElementById('pic-modal').classList.remove('active');
}

async function sha256(str) {
  const enc = new TextEncoder();
  const hashBuf = await crypto.subtle.digest('SHA-256', enc.encode(str));
  return Array.from(new Uint8Array(hashBuf))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

async function submitKey() {
  const enteredKey = document.getElementById('daily-key-input').value.trim().toUpperCase();
  if (!enteredKey) {
    alert("Please enter today's security key.");
    return;
  }

  // Key format: CSE15-MMMDD-XXXXX
  const now = new Date();
  const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
  const todayMonthDay = months[now.getMonth()] + String(now.getDate()).padStart(2, '0');
  
  // Calculate today's exact key token
  const todayYMD = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
  const hashOfToday = await sha256(`${todayYMD}:${MASTER_SALT}`);
  const expectedKey = `CSE15-${todayMonthDay}-${hashOfToday.slice(0, 5).toUpperCase()}`;

  if (enteredKey !== expectedKey) {
    alert("❌ Invalid or expired key!\n\nJoin our Telegram channel to get today's active key, or ask your classmate Arvind Kumar.");
    return;
  }

  // Key is valid! Decrypt student phone number
  if (!guessedStudent || !guessedStudent.enc_phone) {
    alert("No student data available to decrypt.");
    return;
  }

  try {
    const rawPhone = await decryptPhone(guessedStudent.enc_phone, `${MASTER_SALT}:${guessedStudent.roll_no}`);
    
    // Reveal phone
    const phoneDisplay = document.getElementById('vic-phone-display');
    phoneDisplay.innerText = `+91 ${rawPhone}`;
    phoneDisplay.style.color = "#15803d"; // Green

    const unlockBtn = document.getElementById('btn-unlock-trigger');
    unlockBtn.innerText = "✅ Unlocked";
    unlockBtn.disabled = true;

    closeKeyModal();
    alert(`🎉 Key Verified!\nStudent Contact: +91 ${rawPhone}`);
  } catch (err) {
    console.error("Decryption error:", err);
    alert("Decryption failed. Please try again.");
  }
}

async function decryptPhone(hexCipher, key) {
  const enc = new TextEncoder();
  const keyHashBuf = await crypto.subtle.digest('SHA-256', enc.encode(key));
  const keyHash = new Uint8Array(keyHashBuf);

  const cipherBytes = new Uint8Array(hexCipher.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
  const decryptedBytes = new Uint8Array(cipherBytes.length);

  for (let i = 0; i < cipherBytes.length; i++) {
    decryptedBytes[i] = cipherBytes[i] ^ keyHash[i % keyHash.length];
  }

  return new TextDecoder().decode(decryptedBytes);
}
