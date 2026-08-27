/**
 * Main Application Logic for Generator Tugas Random SPSS & Excel
 * Author: Antigravity
 */

// Global State
window.CURRENT_DATASET = null;
window.CURRENT_QUIZ_DATA = [];
window.ALL_BANK_QUESTIONS = [];

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initThemeToggle();
  loadThemes();
  loadCurrentDataset();
  loadQuestionBank();
  loadCheatsheet();
});

// ============================================================================
// 1. TABS & THEME MANAGEMENT
// ============================================================================

function initTabs() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetTab = btn.getAttribute('data-tab');
      const targetPane = document.getElementById(targetTab);
      if (targetPane) targetPane.classList.add('active');
    });
  });
}

function initThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle-btn');
  if (!toggleBtn) return;

  toggleBtn.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    toggleBtn.innerHTML = newTheme === 'dark' ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
  });
}

// ============================================================================
// 2. THEMES & DATASET ENGINE
// ============================================================================

async function loadThemes() {
  try {
    const res = await fetch('/api/themes');
    const data = await res.json();

    const themeSelect = document.getElementById('theme-select');
    if (themeSelect) {
      themeSelect.innerHTML = data.themes.map(t => `
        <option value="${t.id}">${t.name} (${t.category})</option>
      `).join('');
    }

    const catFilterQuiz = document.getElementById('quiz-cat-filter');
    const catFilterBank = document.getElementById('bank-cat-filter');
    if (catFilterQuiz) {
      catFilterQuiz.innerHTML = `<option value="all">Semua Kategori (10 Modul)</option>` + data.categories.map(c => `
        <option value="${c.id}">${c.name}</option>
      `).join('');
    }
    if (catFilterBank) {
      catFilterBank.innerHTML = `<option value="all">Semua Kategori (10 Modul)</option>` + data.categories.map(c => `
        <option value="${c.id}">${c.name}</option>
      `).join('');
    }

  } catch (err) {
    console.error("Error loading themes:", err);
  }
}

async function triggerGenerateDataset() {
  const themeSelect = document.getElementById('theme-select');
  const sampleSizeInput = document.getElementById('sample-size-input');
  const seedInput = document.getElementById('seed-input');

  const theme_id = themeSelect ? themeSelect.value : 'susenas_rt';
  const n_rows = sampleSizeInput ? parseInt(sampleSizeInput.value) : 50;
  const seed = seedInput && seedInput.value ? parseInt(seedInput.value) : null;

  try {
    const res = await fetch('/api/dataset/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ theme_id, n_rows, seed })
    });
    const result = await res.json();
    window.CURRENT_DATASET = result.dataset_summary;
    renderDatasetView(result.dataset_summary);

    // Alert badge
    const badge = document.getElementById('dataset-status-badge');
    if (badge) {
      badge.innerText = `Aktif: ${result.dataset_summary.theme_name} (N=${result.dataset_summary.total_rows})`;
    }

    // Auto trigger new quiz with active dataset
    triggerGenerateQuiz();

  } catch (err) {
    console.error("Error generating dataset:", err);
  }
}

async function loadCurrentDataset() {
  try {
    const res = await fetch('/api/dataset/current');
    const data = await res.json();
    window.CURRENT_DATASET = data;
    renderDatasetView(data);
    triggerGenerateQuiz();
  } catch (err) {
    console.error("Error loading current dataset:", err);
  }
}

function renderDatasetView(data) {
  if (!data) return;

  // Render stats widgets
  document.getElementById('stat-total-rows').innerText = data.total_rows;
  document.getElementById('stat-total-cols').innerText = data.columns.length;
  document.getElementById('stat-theme-name').innerText = data.theme_name;
  document.getElementById('stat-seed-val').innerText = data.seed || '-';

  // Render Column dropdown for visualization
  const colSelect = document.getElementById('chart-col-select');
  if (colSelect) {
    colSelect.innerHTML = data.columns.map(c => `<option value="${c}">${c}</option>`).join('');
    const fullRecords = data.all_data || data.sample_data || [];
    
    colSelect.onchange = () => {
      const selectedCol = colSelect.value;
      const colSummary = data.column_summaries?.[selectedCol];
      const isNum = colSummary?.type === 'numeric';
      renderColumnDistributionChart('chart-canvas', selectedCol, fullRecords, isNum, colSummary);
    };
    // Render first column chart
    if (data.columns.length > 0) {
      const firstCol = data.columns[1] || data.columns[0];
      colSelect.value = firstCol;
      const colSummary = data.column_summaries?.[firstCol];
      const isNum = colSummary?.type === 'numeric';
      renderColumnDistributionChart('chart-canvas', firstCol, fullRecords, isNum, colSummary);
    }
  }

  // Render Table Header & Rows (Preview max 15 rows)
  const tableHead = document.getElementById('dataset-table-head');
  const tableBody = document.getElementById('dataset-table-body');

  if (tableHead) {
    tableHead.innerHTML = `<tr>${data.columns.map(c => `<th>${c}</th>`).join('')}</tr>`;
  }

  if (tableBody) {
    tableBody.innerHTML = data.sample_data.map(row => `
      <tr>${data.columns.map(c => `<td>${formatCellValue(row[c])}</td>`).join('')}</tr>
    `).join('');
  }

  // Render Data Dictionary Sheet view
  const dictContainer = document.getElementById('data-dictionary-list');
  if (dictContainer && data.dictionary) {
    dictContainer.innerHTML = Object.entries(data.dictionary).map(([k, v]) => `
      <div style="display: flex; gap: 12px; padding: 8px 0; border-bottom: 1px solid var(--border-subtle); font-size: 13px;">
        <span class="q-var-tag" style="min-width: 170px;">${k}</span>
        <span style="color: var(--text-secondary);">${v}</span>
      </div>
    `).join('');
  }
}

function formatCellValue(val) {
  if (typeof val === 'number') {
    return Number.isInteger(val) ? val.toLocaleString() : val.toFixed(2);
  }
  return val || '-';
}

function exportActiveDataset(format) {
  window.open(`/api/dataset/export/${format}`, '_blank');
}

// ============================================================================
// 3. DYNAMIC QUIZ & TASK GENERATOR (300 Soal Variatif)
// ============================================================================

async function triggerGenerateQuiz() {
  const countSelect = document.getElementById('quiz-count-select');
  const catFilter = document.getElementById('quiz-cat-filter');
  const diffFilter = document.getElementById('quiz-diff-filter');

  const count = countSelect ? parseInt(countSelect.value) : 10;
  const category_ids = (catFilter && catFilter.value !== 'all') ? [catFilter.value] : null;
  const difficulties = (diffFilter && diffFilter.value !== 'all') ? [diffFilter.value] : null;

  const container = document.getElementById('quiz-questions-container');
  if (container) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px;">
        <i class="fa-solid fa-spinner fa-spin" style="font-size: 32px; color: var(--accent-primary);"></i>
        <p style="margin-top: 10px; color: var(--text-muted);">Sedang menginstansiasi soal acak dari Bank 300 Soal...</p>
      </div>
    `;
  }

  try {
    const res = await fetch('/api/quiz/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ count, category_ids, difficulties })
    });
    const result = await res.json();
    window.CURRENT_QUIZ_DATA = result.questions || [];

    QuestionRenderer.renderQuizList('quiz-questions-container', result.questions);
    resetQuizScoreTracker(result.questions.length);

  } catch (err) {
    console.error("Error generating quiz:", err);
  }
}

function resetQuizScoreTracker(total) {
  document.getElementById('quiz-score-total').innerText = total;
  document.getElementById('quiz-score-answered').innerText = '0';
  document.getElementById('quiz-score-correct').innerText = '0';
  const fill = document.getElementById('quiz-progress-fill');
  if (fill) fill.style.width = '0%';
}

window.updateQuizScoreTracker = function() {
  const correctCards = document.querySelectorAll('.question-card.answered-correct').length;
  const wrongCards = document.querySelectorAll('.question-card.answered-wrong').length;
  const total = window.CURRENT_QUIZ_DATA.length;
  const answered = correctCards + wrongCards;

  document.getElementById('quiz-score-answered').innerText = answered;
  document.getElementById('quiz-score-correct').innerText = correctCards;

  const pct = total > 0 ? (answered / total) * 100 : 0;
  const fill = document.getElementById('quiz-progress-fill');
  if (fill) fill.style.width = `${pct}%`;
};

// ============================================================================
// 4. BANK 300 SOAL CATALOGUE EXPLORER
// ============================================================================

async function loadQuestionBank() {
  try {
    const res = await fetch('/api/questions/bank');
    const data = await res.json();
    window.ALL_BANK_QUESTIONS = data.questions || [];
    renderBankGrid(window.ALL_BANK_QUESTIONS);
  } catch (err) {
    console.error("Error loading question bank:", err);
  }
}

function filterQuestionBank() {
  const searchInput = document.getElementById('bank-search-input');
  const catFilter = document.getElementById('bank-cat-filter');
  const diffFilter = document.getElementById('bank-diff-filter');

  const q = (searchInput?.value || '').toLowerCase();
  const cat = catFilter?.value || 'all';
  const diff = diffFilter?.value || 'all';

  const filtered = window.ALL_BANK_QUESTIONS.filter(item => {
    const matchSearch = item.title.toLowerCase().includes(q) || item.task_text.toLowerCase().includes(q) || item.id.toLowerCase().includes(q);
    const matchCat = (cat === 'all') || (item.cat_id === cat);
    const matchDiff = (diff === 'all') || (item.difficulty === diff);
    return matchSearch && matchCat && matchDiff;
  });

  renderBankGrid(filtered);
}

function renderBankGrid(questions) {
  const grid = document.getElementById('bank-cards-grid');
  if (!grid) return;

  document.getElementById('bank-count-label').innerText = `${questions.length} / 300 Soal`;

  grid.innerHTML = questions.map(q => {
    const diffClass = q.difficulty === 'Mudah' ? 'badge-diff-mudah' : (q.difficulty === 'Sedang' ? 'badge-diff-sedang' : 'badge-diff-sulit');
    return `
      <div class="bank-card">
        <div>
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <span class="badge" style="background: var(--bg-glass-strong); font-family: var(--font-mono);">${q.id}</span>
            <span class="badge ${diffClass}">${q.difficulty}</span>
          </div>
          <h4 style="font-size: 14.5px; font-weight: 700; margin-bottom: 8px; color: var(--text-primary);">${q.title}</h4>
          <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            ${q.task_text.replace(/\{.*?\}/g, '...')}
          </p>
        </div>
        <div style="padding-top: 10px; border-top: 1px solid var(--border-subtle); font-size: 12px; color: var(--accent-cyan);">
          <i class="fa-solid fa-file-excel"></i> ${q.excel_guide || '-'}
        </div>
      </div>
    `;
  }).join('');
}

// ============================================================================
// 5. UNIVERSAL CALCULATOR & VALIDATOR
// ============================================================================

async function runUniversalCalculator() {
  const analysisType = document.getElementById('calc-analysis-type').value;
  const inputX = document.getElementById('calc-input-x').value;
  const inputY = document.getElementById('calc-input-y').value;
  const paramMu0 = parseFloat(document.getElementById('calc-param-mu0').value) || 0;
  const resultBox = document.getElementById('calc-result-box');

  const parseArray = (str) => str.split(/[\s,;\n]+/).map(Number).filter(v => !isNaN(v));
  const data_x = parseArray(inputX);
  const data_y = parseArray(inputY);

  if (data_x.length === 0) {
    alert("Mohon masukkan angka-angka pada Data X.");
    return;
  }

  try {
    const res = await fetch('/api/validator/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        analysis_type: analysisType,
        data_x: data_x,
        data_y: data_y.length > 0 ? data_y : null,
        parameter_mu0: paramMu0
      })
    });

    const result = await res.json();
    resultBox.style.display = 'block';
    resultBox.innerHTML = `
      <div style="font-weight: 700; font-size: 15px; margin-bottom: 10px; color: var(--accent-emerald);">
        <i class="fa-solid fa-circle-check"></i> Hasil Komputasi Internal
      </div>
      <pre style="background: var(--bg-primary); padding: 14px; border-radius: 8px; font-family: var(--font-mono); font-size: 12.5px; overflow-x: auto; color: #a5f3fc;">${JSON.stringify(result, null, 2)}</pre>
    `;
  } catch (err) {
    console.error("Error in calculator:", err);
    alert("Gagal melakukan kalkulasi. Pastikan input data valid.");
  }
}

// ============================================================================
// 6. CHEATSHEET & SPSS NAVIGATION (With SweetAlert-Style Detailed Modals)
// ============================================================================

window.CHEATSHEET_DATA = { excel: [], spss: [] };
window.CURRENT_CHEATSHEET_VIEW = 'all';
window.ACTIVE_MODAL_COPY_TEXT = '';

async function loadCheatsheet() {
  try {
    const res = await fetch('/api/cheatsheet');
    const data = await res.json();
    window.CHEATSHEET_DATA = {
      excel: data.excel_formulas || [],
      spss: data.spss_nav_menus || []
    };

    // Attach search event listeners
    const searchInput = document.getElementById('cheatsheet-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', () => filterCheatsheet());
      searchInput.addEventListener('keyup', () => filterCheatsheet());
      searchInput.addEventListener('search', () => filterCheatsheet());
    }

    // Attach ESC key listener to close modal
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        hideCheatsheetDetailModal();
      }
    });

    renderCheatsheetTables(window.CHEATSHEET_DATA.excel, window.CHEATSHEET_DATA.spss);
  } catch (err) {
    console.error("Error loading cheatsheet:", err);
  }
}

function renderCheatsheetTables(excelList, spssList) {
  const excelBody = document.getElementById('cheatsheet-excel-tbody');
  const spssBody = document.getElementById('cheatsheet-spss-tbody');
  const excelBadge = document.getElementById('excel-count-badge');
  const spssBadge = document.getElementById('spss-count-badge');
  
  // Count Badges
  const countAllBadge = document.getElementById('count-all-badge');
  const countExcelPill = document.getElementById('count-excel-pill');
  const countSpssPill = document.getElementById('count-spss-pill');

  const totalCount = excelList.length + spssList.length;
  if (countAllBadge) countAllBadge.innerText = totalCount;
  if (countExcelPill) countExcelPill.innerText = excelList.length;
  if (countSpssPill) countSpssPill.innerText = spssList.length;

  if (excelBadge) excelBadge.innerText = `${excelList.length} Rumus`;
  if (spssBadge) spssBadge.innerText = `${spssList.length} Menu`;

  // Render Excel Table
  if (excelBody) {
    if (excelList.length === 0) {
      excelBody.innerHTML = `
        <tr>
          <td colspan="5" style="text-align: center; color: var(--text-muted); padding: 28px;">
            <i class="fa-solid fa-folder-open" style="font-size: 24px; margin-bottom: 8px; display: block; opacity: 0.5;"></i>
            Tidak ada rumus Excel yang cocok dengan pencarian kata kunci tersebut.
          </td>
        </tr>
      `;
    } else {
      excelBody.innerHTML = excelList.map(row => `
        <tr class="table-clickable-row" onclick="showExcelDetail('${row.id}')" title="Klik untuk melihat penjelasan detail & contoh formula">
          <td><span class="badge badge-cat">${row.category}</span></td>
          <td><strong style="color: var(--text-primary); font-size: 13.5px;">${row.name}</strong></td>
          <td><code style="color: #60a5fa; font-family: var(--font-mono); font-weight: 600; background: rgba(96, 165, 250, 0.1); padding: 3px 7px; border-radius: 4px; border: 1px solid rgba(96, 165, 250, 0.2); font-size: 12.5px;">${row.formula}</code></td>
          <td style="color: var(--text-secondary); font-size: 12px; white-space: normal; min-width: 140px;">${row.note}</td>
          <td style="text-align: center;" onclick="event.stopPropagation()">
            <button class="btn-detail-sm btn-detail-excel" onclick="showExcelDetail('${row.id}')" title="Lihat Panduan Detail">
              <i class="fa-solid fa-circle-info"></i> Detail
            </button>
          </td>
        </tr>
      `).join('');
    }
  }

  // Render SPSS Table
  if (spssBody) {
    if (spssList.length === 0) {
      spssBody.innerHTML = `
        <tr>
          <td colspan="4" style="text-align: center; color: var(--text-muted); padding: 28px;">
            <i class="fa-solid fa-folder-open" style="font-size: 24px; margin-bottom: 8px; display: block; opacity: 0.5;"></i>
            Tidak ada menu SPSS yang cocok dengan pencarian kata kunci tersebut.
          </td>
        </tr>
      `;
    } else {
      spssBody.innerHTML = spssList.map(row => {
        // Format path with interactive chevron breadcrumbs
        const pathFormatted = (row.menu_path || '')
          .split(' > ')
          .map(part => `<span class="spss-path-step">${part}</span>`)
          .join('<i class="fa-solid fa-chevron-right spss-path-arrow"></i>');

        return `
          <tr class="table-clickable-row" onclick="showSpssDetail('${row.id}')" title="Klik untuk membuka panduan langkah demi langkah SPSS & cara interpretasi output">
            <td>
              <div style="font-weight: 700; color: var(--text-primary); font-size: 13.5px; margin-bottom: 4px;">
                ${row.analysis}
              </div>
              <span class="badge" style="background: rgba(244, 114, 182, 0.12); color: #f472b6; font-size: 10.5px;">
                ${row.category || 'Statistik'}
              </span>
            </td>
            <td><div class="spss-path-badge">${pathFormatted}</div></td>
            <td style="color: var(--text-secondary); font-size: 12px; white-space: normal; min-width: 150px; line-height: 1.45;">
              ${row.output_key}
            </td>
            <td style="text-align: center;" onclick="event.stopPropagation()">
              <button class="btn-detail-sm" onclick="showSpssDetail('${row.id}')" title="Buka Pop-up Penjelasan Detail SPSS">
                <i class="fa-solid fa-circle-info"></i> Detail Panduan
              </button>
            </td>
          </tr>
        `;
      }).join('');
    }
  }
}

function filterCheatsheet() {
  const searchInput = document.getElementById('cheatsheet-search-input');
  const clearBtn = document.getElementById('cheatsheet-clear-search-btn');
  const q = (searchInput?.value || '').toLowerCase().trim();

  if (clearBtn) {
    clearBtn.style.display = q.length > 0 ? 'inline-flex' : 'none';
  }

  const filteredExcel = (window.CHEATSHEET_DATA.excel || []).filter(item => {
    if (!q) return true;
    const str = [
      item.category, item.name, item.formula, item.note, 
      item.purpose, item.syntax, item.example, item.tips
    ].filter(Boolean).join(' ').toLowerCase();
    return str.includes(q);
  });

  const filteredSpss = (window.CHEATSHEET_DATA.spss || []).filter(item => {
    if (!q) return true;
    const str = [
      item.analysis, item.category, item.menu_path, item.output_key,
      item.purpose, item.assumptions, item.decision_rule, item.example_case,
      item.spss_syntax, ...(item.detailed_steps || [])
    ].filter(Boolean).join(' ').toLowerCase();
    return str.includes(q);
  });

  renderCheatsheetTables(filteredExcel, filteredSpss);
}

function clearCheatsheetSearch() {
  const searchInput = document.getElementById('cheatsheet-search-input');
  if (searchInput) {
    searchInput.value = '';
    searchInput.focus();
  }
  filterCheatsheet();
}

function switchCheatsheetView(mode) {
  window.CURRENT_CHEATSHEET_VIEW = mode;
  const excelCard = document.getElementById('cheatsheet-excel-card');
  const spssCard = document.getElementById('cheatsheet-spss-card');
  const container = document.getElementById('cheatsheet-container');
  const btnAll = document.getElementById('btn-show-all-cheatsheet');
  const btnExcel = document.getElementById('btn-show-excel-cheatsheet');
  const btnSpss = document.getElementById('btn-show-spss-cheatsheet');

  [btnAll, btnExcel, btnSpss].forEach(b => b && b.classList.remove('active'));

  if (mode === 'all') {
    if (btnAll) btnAll.classList.add('active');
    if (excelCard) excelCard.style.display = 'block';
    if (spssCard) spssCard.style.display = 'block';
    if (container) container.style.gridTemplateColumns = '';
  } else if (mode === 'excel') {
    if (btnExcel) btnExcel.classList.add('active');
    if (excelCard) excelCard.style.display = 'block';
    if (spssCard) spssCard.style.display = 'none';
    if (container) container.style.gridTemplateColumns = '1fr';
  } else if (mode === 'spss') {
    if (btnSpss) btnSpss.classList.add('active');
    if (excelCard) excelCard.style.display = 'none';
    if (spssCard) spssCard.style.display = 'block';
    if (container) container.style.gridTemplateColumns = '1fr';
  }
}

// ============================================================================
// 7. SWEETALERT-STYLE STATISTICAL GUIDE POP-UP MODAL
// ============================================================================

function showSpssDetail(itemId) {
  const item = (window.CHEATSHEET_DATA.spss || []).find(x => x.id === itemId);
  if (!item) return;

  const modal = document.getElementById('cheatsheet-detail-modal');
  const iconContainer = document.getElementById('swal-icon-container');
  const badgeEl = document.getElementById('swal-modal-badge');
  const titleEl = document.getElementById('swal-modal-title');
  const contentEl = document.getElementById('swal-modal-content');
  const copyTextEl = document.getElementById('swal-copy-text');

  if (iconContainer) {
    iconContainer.className = 'swal-icon-circle';
    iconContainer.innerHTML = '<i class="fa-solid fa-calculator"></i>';
  }
  if (badgeEl) {
    badgeEl.className = 'swal-badge';
    badgeEl.innerHTML = `<i class="fa-solid fa-bolt"></i> IBM SPSS: ${item.category || 'Komparatif'}`;
  }
  if (titleEl) {
    titleEl.innerText = item.analysis;
  }
  if (copyTextEl) {
    copyTextEl.innerText = "Salin Panduan & Sintaks";
  }

  // Format steps timeline
  const stepsHtml = (item.detailed_steps || []).map((step, idx) => `
    <li class="swal-step-item">
      <span class="swal-step-num">${idx + 1}</span>
      <div>${step.replace(/➔/g, '<i class="fa-solid fa-chevron-right" style="color: #f472b6; font-size: 10px; margin: 0 4px;"></i>')}</div>
    </li>
  `).join('');

  // Format modal body
  contentEl.innerHTML = `
    <!-- 1. Tujuan Analisis -->
    <div class="swal-section-block">
      <div class="swal-section-title">
        <i class="fa-solid fa-bullseye" style="color: #ec4899;"></i> 1. Tujuan & Kapan Digunakan
      </div>
      <div class="swal-section-desc">
        ${item.purpose}
      </div>
      ${item.assumptions ? `
        <div style="margin-top: 10px; padding-top: 8px; border-top: 1px dashed var(--border-subtle); font-size: 12.5px; color: var(--accent-amber);">
          <strong><i class="fa-solid fa-triangle-exclamation"></i> Syarat & Asumsi Uji:</strong> ${item.assumptions}
        </div>
      ` : ''}
    </div>

    <!-- 2. Langkah Navigasi Menu SPSS -->
    <div class="swal-section-block">
      <div class="swal-section-title">
        <i class="fa-solid fa-diagram-project" style="color: #8b5cf6;"></i> 2. Jalur Menu & Langkah Klik Detail
      </div>
      <div style="margin-bottom: 14px;">
        <span style="font-size: 12px; color: var(--text-muted); display: block; margin-bottom: 4px;">Jalur Cepat Menu:</span>
        <div class="spss-path-badge" style="font-size: 12.5px; padding: 6px 12px;">
          ${item.menu_path.split(' > ').map(p => `<span class="spss-path-step">${p}</span>`).join('<i class="fa-solid fa-chevron-right spss-path-arrow"></i>')}
        </div>
      </div>
      <ol class="swal-steps-timeline">
        ${stepsHtml}
      </ol>
    </div>

    <!-- 3. Output Utama & Pengambilan Keputusan -->
    <div class="swal-section-block">
      <div class="swal-section-title">
        <i class="fa-solid fa-scale-balanced" style="color: #10b981;"></i> 3. Output Kunci & Kriteria Keputusan
      </div>
      <div style="font-size: 13px; margin-bottom: 10px;">
        <strong style="color: var(--text-primary);">Tabel Output Utama:</strong> 
        <span style="color: var(--text-secondary);">${item.output_key}</span>
      </div>
      <div class="swal-callout-box">
        <strong style="display: block; margin-bottom: 4px; color: var(--accent-primary);"><i class="fa-solid fa-gavel"></i> Kaidah Keputusan Hipotesis (Signifikansi):</strong>
        ${(item.decision_rule || '').replace(/\\n/g, '<br>')}
      </div>
    </div>

    <!-- 4. Contoh Kasus Riil & Sintaks SPSS -->
    ${item.example_case ? `
      <div class="swal-section-block">
        <div class="swal-section-title">
          <i class="fa-solid fa-lightbulb" style="color: #fbbf24;"></i> 4. Contoh Kasus Praktik
        </div>
        <div class="swal-section-desc">
          ${item.example_case}
        </div>
        ${item.spss_syntax ? `
          <div style="margin-top: 12px;">
            <span style="font-size: 11.5px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Kode Sintaks SPSS (.sps):</span>
            <div class="swal-code-box" style="margin-top: 4px;">${item.spss_syntax}</div>
          </div>
        ` : ''}
      </div>
    ` : ''}
  `;

  // Prepare clipboard copy text
  window.ACTIVE_MODAL_COPY_TEXT = `PANDUAN IBM SPSS: ${item.analysis}
Kategori: ${item.category}
Jalur Menu: ${item.menu_path}

Tujuan:
${item.purpose}

Langkah-langkah:
${(item.detailed_steps || []).map((s, i) => `${i + 1}. ${s}`).join('\n')}

Kaidah Keputusan:
${(item.decision_rule || '').replace(/\\n/g, '\n')}

Sintaks SPSS:
${item.spss_syntax || '-'}`;

  if (modal) modal.classList.add('active');
}

function showExcelDetail(itemId) {
  const item = (window.CHEATSHEET_DATA.excel || []).find(x => x.id === itemId);
  if (!item) return;

  const modal = document.getElementById('cheatsheet-detail-modal');
  const iconContainer = document.getElementById('swal-icon-container');
  const badgeEl = document.getElementById('swal-modal-badge');
  const titleEl = document.getElementById('swal-modal-title');
  const contentEl = document.getElementById('swal-modal-content');
  const copyTextEl = document.getElementById('swal-copy-text');

  if (iconContainer) {
    iconContainer.className = 'swal-icon-circle excel-theme';
    iconContainer.innerHTML = '<i class="fa-solid fa-file-excel"></i>';
  }
  if (badgeEl) {
    badgeEl.className = 'swal-badge excel-badge';
    badgeEl.innerHTML = `<i class="fa-solid fa-calculator"></i> Excel: ${item.category || 'Formula'}`;
  }
  if (titleEl) {
    titleEl.innerText = item.name;
  }
  if (copyTextEl) {
    copyTextEl.innerText = "Salin Formula";
  }

  contentEl.innerHTML = `
    <!-- 1. Formula & Sintaks -->
    <div class="swal-section-block">
      <div class="swal-section-title">
        <i class="fa-solid fa-code" style="color: #10b981;"></i> 1. Sintaks Formula Excel
      </div>
      <div class="swal-code-box" style="font-size: 14px; color: #34d399;">
        ${item.formula}
      </div>
      ${item.syntax ? `
        <div style="margin-top: 8px; font-size: 12.5px; color: var(--text-muted);">
          <strong>Struktur Lengkap:</strong> <code style="color: #60a5fa;">${item.syntax}</code>
        </div>
      ` : ''}
    </div>

    <!-- 2. Tujuan & Penjelasan -->
    <div class="swal-section-block">
      <div class="swal-section-title">
        <i class="fa-solid fa-circle-question" style="color: #38bdf8;"></i> 2. Penjelasan & Kegunaan
      </div>
      <div class="swal-section-desc">
        ${item.purpose || item.note}
      </div>
    </div>

    <!-- 3. Contoh Penggunaan -->
    <div class="swal-section-block">
      <div class="swal-section-title">
        <i class="fa-solid fa-table" style="color: #fbbf24;"></i> 3. Contoh Penerapan Nyata
      </div>
      <div class="swal-callout-box" style="border-left-color: #10b981; background: rgba(16, 185, 129, 0.08);">
        ${item.example || `Contoh: ${item.formula}`}
      </div>
      ${item.tips ? `
        <div style="margin-top: 12px; font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
          <strong style="color: var(--accent-emerald);"><i class="fa-solid fa-lightbulb"></i> Tips Praktis:</strong> ${item.tips}
        </div>
      ` : ''}
    </div>
  `;

  window.ACTIVE_MODAL_COPY_TEXT = item.formula;
  if (modal) modal.classList.add('active');
}

function hideCheatsheetDetailModal() {
  const modal = document.getElementById('cheatsheet-detail-modal');
  if (modal) modal.classList.remove('active');
}

function closeCheatsheetModal(event) {
  if (event.target.id === 'cheatsheet-detail-modal') {
    hideCheatsheetDetailModal();
  }
}

async function copyCheatsheetSteps() {
  const textToCopy = window.ACTIVE_MODAL_COPY_TEXT;
  if (!textToCopy) return;

  try {
    await navigator.clipboard.writeText(textToCopy);
    const copyText = document.getElementById('swal-copy-text');
    if (copyText) {
      const original = copyText.innerText;
      copyText.innerText = "Tersalin! ✅";
      setTimeout(() => {
        if (copyText) copyText.innerText = original;
      }, 2000);
    }
  } catch (err) {
    console.error("Gagal menyalin:", err);
  }
}

// Make functions globally available for inline onclick handlers
window.filterCheatsheet = filterCheatsheet;
window.clearCheatsheetSearch = clearCheatsheetSearch;
window.switchCheatsheetView = switchCheatsheetView;
window.showSpssDetail = showSpssDetail;
window.showExcelDetail = showExcelDetail;
window.hideCheatsheetDetailModal = hideCheatsheetDetailModal;
window.closeCheatsheetModal = closeCheatsheetModal;
window.copyCheatsheetSteps = copyCheatsheetSteps;

// Print / Export Quiz to Printable Document
function printQuizTasks() {
  window.print();
}


