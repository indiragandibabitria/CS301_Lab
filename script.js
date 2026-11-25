// Storage Key
const STORAGE_KEY = 'journal_entries';

// Main Selectors
const openModalBtn = document.getElementById('openModalBtn');
const closeModalBtn = document.getElementById('cancelBtn');
const saveModalBtn = document.getElementById('saveBtn');
const modal = document.getElementById('entryModal');

const titleInput = document.getElementById('entryTitle');
const bodyInput = document.getElementById('entryBody');
const entriesList = document.getElementById('entriesList');

const entryCountEl = document.getElementById('entryCount');
const wordCountEl = document.getElementById('wordCount');
const dayCountEl = document.getElementById('dayCount');

// Insights Modal Selectors
const statsContainer = document.getElementById('statsContainer');
const insightsModal = document.getElementById('insightsModal');
const closeInsightsBtn = document.getElementById('closeInsightsBtn');
const insightEntryCount = document.getElementById('insightEntryCount');

// Default Entries
let entries = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [
  {
    id: 1,
    title: 'Gym',
    body: 'Worked out today.',
    date: 'Wednesday, Oct 14',
    rawDate: new Date().toISOString()
  }
];

function saveToLocalStorage() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
}

function updateStats() {
  const totalEntries = entries.length;
  let totalWords = 0;
  const uniqueDays = new Set();

  entries.forEach(entry => {
    const text = `${entry.title} ${entry.body}`.trim();
    totalWords += text ? text.split(/\s+/).length : 0;
    uniqueDays.add(entry.date);
  });

  entryCountEl.textContent = totalEntries;
  wordCountEl.textContent = totalWords;
  dayCountEl.textContent = uniqueDays.size;
  
  // Also sync Insights Big Number
  insightEntryCount.textContent = totalEntries;
}

function renderEntries() {
  entriesList.innerHTML = '';

  entries.forEach((entry, index) => {
    const card = document.createElement('div');
    card.className = 'entry-card';
    card.innerHTML = `
      <div class="entry-title">${entry.title}</div>
      ${entry.body ? `<div class="entry-body" style="font-size:14px; color:#3c3c43; margin-bottom:10px;">${entry.body}</div>` : ''}
      <div class="entry-footer">
        <span>${entry.date}</span>
        <i class="fa-solid fa-trash-can" onclick="deleteEntry(${index})" style="cursor:pointer; color:#8e8e93;"></i>
      </div>
    `;
    entriesList.appendChild(card);
  });

  updateStats();
}

function deleteEntry(index) {
  if (confirm('Delete this entry?')) {
    entries.splice(index, 1);
    saveToLocalStorage();
    renderEntries();
  }
}

function formatDate(d) {
  const options = { weekday: 'long', month: 'short', day: 'numeric' };
  return d.toLocaleDateString('en-US', options);
}

// Click on Stats Card to open Insights view
statsContainer.addEventListener('click', () => {
  insightsModal.classList.add('active');
});

// Close Insights view
closeInsightsBtn.addEventListener('click', () => {
  insightsModal.classList.remove('active');
});

// Modal Actions
openModalBtn.addEventListener('click', () => modal.classList.add('active'));

closeModalBtn.addEventListener('click', () => {
  modal.classList.remove('active');
  titleInput.value = '';
  bodyInput.value = '';
});

saveModalBtn.addEventListener('click', () => {
  const title = titleInput.value.trim();
  const body = bodyInput.value.trim();

  if (!title) return alert('Please enter a title');

  const newEntry = {
    id: Date.now(),
    title: title,
    body: body,
    date: formatDate(new Date()),
    rawDate: new Date().toISOString()
  };

  entries.unshift(newEntry);
  saveToLocalStorage();
  renderEntries();

  modal.classList.remove('active');
  titleInput.value = '';
  bodyInput.value = '';
});

// Initial Render
renderEntries();