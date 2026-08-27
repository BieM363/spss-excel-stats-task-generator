/**
 * Question Card Renderer & Quiz Interactive Controller
 * Author: BieM363 (https://github.com/BieM363)
 */

const QuestionRenderer = {
  renderQuizList(containerId, questions) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!questions || questions.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 40px; color: var(--text-muted);">
          <i class="fa-solid fa-clipboard-question" style="font-size: 36px; margin-bottom: 12px; display: block;"></i>
          <p>Belum ada soal yang di-generate. Klik tombol <strong>'Mulai Latihan Baru'</strong> di atas.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = questions.map((q, idx) => this.renderSingleCard(q, idx)).join('');
  },

  renderSingleCard(q, idx) {
    const diffClass = q.difficulty === 'Mudah' ? 'badge-diff-mudah' : (q.difficulty === 'Sedang' ? 'badge-diff-sedang' : 'badge-diff-sulit');

    // Highlight bracketed variables e.g. [Variabel]
    const formattedTask = q.task_text.replace(/\[(.*?)\]/g, `<span class="q-var-tag">$1</span>`);

    return `
      <div class="question-card" id="qcard-${q.id}-${idx}">
        <div class="q-meta">
          <span class="badge" style="background: var(--bg-glass-strong); color: var(--text-primary);">
            Soal #${idx + 1}
          </span>
          <span class="badge badge-cat">
            <i class="fa-solid fa-tag"></i> ${q.cat_id}
          </span>
          <span class="badge ${diffClass}">
            <i class="fa-solid fa-gauge-high"></i> ${q.difficulty}
          </span>
          <span style="margin-left: auto; font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">
            ID: ${q.id}
          </span>
        </div>

        <div class="q-title">${q.title}</div>
        
        <div class="q-prompt">
          ${formattedTask}
        </div>

        <button class="hint-toggle-btn" onclick="QuestionRenderer.toggleHint('hint-${q.id}-${idx}')">
          <i class="fa-solid fa-lightbulb"></i> Buka Bantuan SPSS & Excel
        </button>

        <div class="hint-box" id="hint-${q.id}-${idx}">
          <div class="hint-line">
            <span class="hint-badge"><i class="fa-solid fa-file-excel"></i> Rumus Excel</span>
            <code style="color: #60a5fa; font-family: var(--font-mono);">${q.excel_guide || '-'}</code>
          </div>
          <div class="hint-line">
            <span class="hint-badge hint-badge-spss"><i class="fa-solid fa-calculator"></i> Menu SPSS</span>
            <span style="color: #f472b6;">${q.spss_guide || '-'}</span>
          </div>
          ${q.task_instruction ? `<div style="margin-top: 6px; font-size: 12px; color: var(--text-muted);"><i class="fa-solid fa-info-circle"></i> ${q.task_instruction}</div>` : ''}
        </div>

        <div class="answer-action-box">
          <div class="answer-input-wrapper">
            <input type="text" 
                   class="form-input" 
                   id="input-${q.id}-${idx}" 
                   placeholder="Ketik jawaban Anda..." 
                   onkeydown="if(event.key === 'Enter') QuestionRenderer.checkAnswer('${q.id}', ${idx})" />
          </div>

          <button class="btn btn-primary" onclick="QuestionRenderer.checkAnswer('${q.id}', ${idx})">
            <i class="fa-solid fa-circle-check"></i> Periksa Jawaban
          </button>

          <span style="font-size: 12px; color: var(--text-muted);">
            (Toleransi pembulatan ±${q.tolerance})
          </span>
        </div>

        <div class="solution-panel" id="sol-${q.id}-${idx}"></div>
      </div>
    `;
  },

  toggleHint(hintId) {
    const box = document.getElementById(hintId);
    if (box) {
      box.classList.toggle('open');
    }
  },

  async checkAnswer(qId, idx) {
    const inputEl = document.getElementById(`input-${qId}-${idx}`);
    const cardEl = document.getElementById(`qcard-${qId}-${idx}`);
    const solPanel = document.getElementById(`sol-${qId}-${idx}`);

    if (!inputEl) return;
    const userAnswer = inputEl.value.trim();

    if (!userAnswer) {
      alert("Silakan ketikkan jawaban Anda terlebih dahulu.");
      return;
    }

    const currentQuiz = window.CURRENT_QUIZ_DATA || [];
    const qObj = currentQuiz[idx];
    if (!qObj) return;

    try {
      const response = await fetch('/api/quiz/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question_id: qId,
          user_answer: userAnswer,
          expected_value: qObj.expected_value,
          tolerance: qObj.tolerance,
          ground_truth_details: qObj.ground_truth_details
        })
      });

      const result = await response.json();

      // Update Card Styling
      cardEl.classList.remove('answered-correct', 'answered-wrong');
      solPanel.classList.remove('correct', 'wrong');

      if (result.is_correct) {
        cardEl.classList.add('answered-correct');
        solPanel.classList.add('correct');
      } else {
        cardEl.classList.add('answered-wrong');
        solPanel.classList.add('wrong');
      }

      // Format steps if available
      const details = result.solution_details?.details || {};
      const steps = details.steps || [];
      const conclusion = details.conclusion || '';

      solPanel.innerHTML = `
        <div style="font-weight: 700; margin-bottom: 6px; display: flex; align-items: center; gap: 8px;">
          <i class="fa-solid ${result.is_correct ? 'fa-check-circle' : 'fa-times-circle'}"></i>
          ${result.feedback_message}
        </div>
        <div style="margin-bottom: 6px;">
          <strong>Nilai Eksak Komputasi:</strong> <span style="font-family: var(--font-mono); font-weight: 700;">${result.expected_answer}</span>
          ${details.formula_tex ? `<div style="margin: 4px 0; color: var(--text-muted); font-size: 12px;">Rumus: <code>${details.formula_tex}</code></div>` : ''}
        </div>
        ${steps.length > 0 ? `
          <div style="font-weight: 600; margin-top: 8px;">Langkah Penyelesaian Matematis:</div>
          <ol class="steps-list">
            ${steps.map(s => `<li>${s}</li>`).join('')}
          </ol>
        ` : ''}
        ${conclusion ? `<div style="margin-top: 6px; padding: 8px 12px; background: var(--bg-glass-strong); border-radius: 6px;"><strong>Interpretasi / Kesimpulan:</strong> ${conclusion}</div>` : ''}
      `;

      // Update Quiz progress bar and score
      window.updateQuizScoreTracker && window.updateQuizScoreTracker();

    } catch (err) {
      console.error("Error checking answer:", err);
      alert("Gagal memvalidasi jawaban ke server.");
    }
  }
};
