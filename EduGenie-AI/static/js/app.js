const featureSelect = document.getElementById('feature');
const inputLabel = document.getElementById('input-label');
const textInput = document.getElementById('text-input');
const submitBtn = document.getElementById('submit-btn');
const statusBox = document.getElementById('status');
const resultBox = document.getElementById('result');
const emptyState = document.getElementById('empty-state');
const charCount = document.getElementById('character-count');

const featureConfig = {
  qa: {
    label: 'Question',
    placeholder: 'Ask a learning question...',
    endpoint: '/qa',
    payloadKey: 'question',
    responseKey: 'answer',
    buttonText: 'Ask'
  },
  explain: {
    label: 'Topic to explain',
    placeholder: 'Explain photosynthesis, fractions, etc.',
    endpoint: '/explain',
    payloadKey: 'topic',
    responseKey: 'explanation',
    buttonText: 'Explain'
  },
  quiz: {
    label: 'Study material',
    placeholder: 'Paste a lesson or text to create a quiz...',
    endpoint: '/quiz',
    payloadKey: 'text',
    responseKey: 'quiz',
    buttonText: 'Create Quiz'
  },
  summarize: {
    label: 'Text to summarize',
    placeholder: 'Paste the text you want summarized...',
    endpoint: '/summarize',
    payloadKey: 'text',
    responseKey: 'summary',
    buttonText: 'Summarize'
  },
  learn: {
    label: 'Topic and level',
    placeholder: 'Example: "Python" with level beginner',
    endpoint: '/learn/recommendations',
    payloadKey: 'topic',
    responseKey: 'recommendations',
    buttonText: 'Generate plan'
  }
};

function updateFeatureUI() {
  const current = featureConfig[featureSelect.value];
  inputLabel.textContent = current.label;
  textInput.placeholder = current.placeholder;
  submitBtn.textContent = current.buttonText;
  const currentValue = textInput.value.trim();
  charCount.textContent = `${currentValue.length} characters`;
}

featureSelect.addEventListener('change', updateFeatureUI);
textInput.addEventListener('input', () => {
  charCount.textContent = `${textInput.value.length} characters`;
});

function showStatus(message, isError = false) {
  statusBox.textContent = message;
  statusBox.classList.toggle('error', isError);
}

function renderResult(raw) {
  emptyState.hidden = true;
  resultBox.hidden = false;

  if (Array.isArray(raw)) {
    resultBox.innerHTML = raw
      .map((item, index) => {
        const options = item.options.map((opt) => `<li>${opt}</li>`).join('');
        return `
          <div class="quiz-question">
            <h3>${index + 1}. ${item.question}</h3>
            <ul>${options}</ul>
            <div class="feedback"><strong>Answer:</strong> ${item.answer}<br><strong>Explanation:</strong> ${item.explanation}</div>
          </div>
        `;
      })
      .join('');
    return;
  }

  resultBox.textContent = String(raw);
}

submitBtn.addEventListener('click', async () => {
  const config = featureConfig[featureSelect.value];
  const value = textInput.value.trim();

  if (!value) {
    showStatus('Please enter some content before submitting.', true);
    return;
  }

  showStatus('Generating response...');
  submitBtn.disabled = true;

  try {
    let payload = { [config.payloadKey]: value };

    if (featureSelect.value === 'learn') {
      const level = prompt('Enter learner level (beginner, intermediate, advanced):', 'beginner');
      payload = {
        topic: value,
        level: (level || 'beginner').trim().toLowerCase()
      };
    }

    const response = await fetch(config.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Request failed');
    }

    const output = data[config.responseKey];
    renderResult(output);
    showStatus('Done.');
  } catch (error) {
    showStatus(error.message || 'Something went wrong.', true);
    resultBox.hidden = false;
    resultBox.textContent = 'Unable to generate a response right now.';
  } finally {
    submitBtn.disabled = false;
  }
});

updateFeatureUI();
