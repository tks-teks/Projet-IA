import { initAvatar, setAvatarState } from './avatar/avatar.js';

const API_BASE = 'http://localhost:8000';
const ws = new WebSocket('ws://localhost:8000/ws');

const micBtn = document.getElementById('micBtn');
const speakBtn = document.getElementById('speakBtn');
const muteBtn = document.getElementById('muteBtn');
const transcriptEl = document.getElementById('transcript');
const replyEl = document.getElementById('assistantReply');
const statusEl = document.getElementById('assistantStatus');
const avatarStateEl = document.getElementById('avatarState');
const alertsTable = document.getElementById('alertsTable');

let isListening = false;
let isMuted = false;
let activated = false;
let lastAutoSpeech = 0;

initAvatar('avatarCanvas');

const alertsChart = new Chart(document.getElementById('alertsChart'), {
  type: 'bar',
  data: {
    labels: ['CRITICAL', 'HIGH', 'MEDIUM'],
    datasets: [{
      label: 'Alertes',
      data: [0, 0, 0],
      backgroundColor: ['#ef4444', '#f97316', '#facc15']
    }]
  },
  options: { responsive: true, plugins: { legend: { display: false } } }
});

const eventsChart = new Chart(document.getElementById('eventsChart'), {
  type: 'line',
  data: {
    labels: ['-5m', '-4m', '-3m', '-2m', '-1m', 'maintenant'],
    datasets: [{
      label: 'Événements',
      data: [4, 6, 5, 7, 8, 6],
      borderColor: '#38bdf8',
      backgroundColor: 'rgba(56,189,248,0.2)'
    }]
  },
  options: { responsive: true, plugins: { legend: { display: false } } }
});

function updateAvatarState(state) {
  setAvatarState(state);
  avatarStateEl.textContent = `State: ${state}`;
}

function speak(text, auto = false) {
  if (isMuted) return;
  if (auto) {
    const now = Date.now();
    if (now - lastAutoSpeech < 30000) return;
    lastAutoSpeech = now;
  }
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'fr-FR';
  utterance.onstart = () => updateAvatarState('talking');
  utterance.onend = () => updateAvatarState('idle');
  speechSynthesis.speak(utterance);
}

function addAlertRow(alert) {
  const row = document.createElement('tr');
  row.innerHTML = `
    <td class="py-2">${alert.id}</td>
    <td class="py-2 text-${alert.severity === 'CRITICAL' ? 'red' : 'orange'}-400">${alert.severity}</td>
    <td class="py-2">${alert.title}</td>
    <td class="py-2 text-slate-400">${alert.description}</td>
  `;
  alertsTable.prepend(row);
}

function incrementAlertChart(severity) {
  const index = { CRITICAL: 0, HIGH: 1, MEDIUM: 2 }[severity] ?? 2;
  alertsChart.data.datasets[0].data[index] += 1;
  alertsChart.update();
}

async function sendQuery(text) {
  const response = await fetch(`${API_BASE}/assistant/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, context: {} })
  });
  const data = await response.json();
  replyEl.textContent = data.reply;
  speak(data.reply);
  statusEl.textContent = `Intent: ${data.intent} (${data.confidence})`;
}

function handleTranscript(text) {
  transcriptEl.textContent = text;
  const lower = text.toLowerCase();
  if (lower.includes('khelia')) {
    activated = true;
    const cleaned = lower.replace('khelia', '').trim();
    sendQuery(cleaned || 'statut');
    return;
  }
  if (!activated) {
    statusEl.textContent = 'Dites "KHELIA" pour activer.';
    return;
  }
  sendQuery(text);
}

let recognition;
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.lang = 'fr-FR';
  recognition.continuous = false;
  recognition.interimResults = true;

  recognition.onstart = () => {
    isListening = true;
    statusEl.textContent = 'Écoute active...';
    updateAvatarState('listening');
  };

  recognition.onend = () => {
    isListening = false;
    statusEl.textContent = 'Micro arrêté.';
    updateAvatarState('idle');
  };

  recognition.onresult = (event) => {
    const transcript = Array.from(event.results)
      .map((result) => result[0].transcript)
      .join(' ');
    handleTranscript(transcript);
  };
} else {
  statusEl.textContent = 'STT indisponible dans ce navigateur.';
}

micBtn.addEventListener('click', () => {
  if (!recognition) return;
  if (isListening) {
    recognition.stop();
  } else {
    recognition.start();
  }
});

speakBtn.addEventListener('click', () => {
  speak(replyEl.textContent || 'Prête à répondre.');
});

muteBtn.addEventListener('click', () => {
  isMuted = !isMuted;
  muteBtn.textContent = isMuted ? 'Unmute' : 'Mute';
});

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'new_alert') {
    const alert = message.data;
    addAlertRow(alert);
    incrementAlertChart(alert.severity);
    if (alert.severity === 'CRITICAL') {
      updateAvatarState('alert');
      speak(`Alerte critique détectée : ${alert.title}`, true);
    }
  }
  if (message.type === 'assistant_say') {
    const payload = message.data;
    updateAvatarState('alert');
    speak(payload.text, true);
  }
};
