/**
 * Enhanced Chart.js Visualizer for Generator Tugas Random SPSS & Excel
 * Author: BieM363 (https://github.com/BieM363)
 * Provides dynamic categorical pie/doughnut and numerical histogram distribution
 * with complete summary metrics & frequency breakdown.
 */

let activeChartInstance = null;

function renderColumnDistributionChart(canvasId, colName, sampleData, isNumeric, colSummary) {
  const canvas = document.getElementById(canvasId);
  const detailsPanel = document.getElementById('chart-details-panel');
  const typeBadge = document.getElementById('chart-type-badge');
  const iconBadge = document.getElementById('chart-icon-badge');

  if (!canvas) return;

  // Destroy previous chart instance and clean canvas attributes
  if (activeChartInstance) {
    activeChartInstance.destroy();
    activeChartInstance = null;
  }
  canvas.removeAttribute('width');
  canvas.removeAttribute('height');
  canvas.style.width = '100%';
  canvas.style.height = '100%';

  // Extract raw non-null values
  const rawValues = sampleData
    .map(row => row[colName])
    .filter(v => v !== null && v !== undefined && v !== '');

  const totalN = rawValues.length;

  if (isNumeric) {
    // -------------------------------------------------------------------------
    // NUMERICAL COLUMN: HISTOGRAM & DESCRIPTIVE STATS
    // -------------------------------------------------------------------------
    if (typeBadge) {
      typeBadge.className = 'col-type-pill pill-numeric';
      typeBadge.innerHTML = '<i class="fa-solid fa-arrow-trend-up"></i> Numerik (Kuantitatif)';
    }
    if (iconBadge) {
      iconBadge.innerHTML = '<i class="fa-solid fa-chart-column"></i>';
      iconBadge.style.background = 'linear-gradient(135deg, #6366f1, #3b82f6)';
    }

    const numValues = rawValues.map(Number).filter(v => !isNaN(v));
    numValues.sort((a, b) => a - b);

    const min = numValues.length > 0 ? numValues[0] : 0;
    const max = numValues.length > 0 ? numValues[numValues.length - 1] : 0;
    const sum = numValues.reduce((acc, cur) => acc + cur, 0);
    const mean = numValues.length > 0 ? sum / numValues.length : 0;

    // Calculate median
    let median = 0;
    const n = numValues.length;
    if (n > 0) {
      median = n % 2 === 1 ? numValues[Math.floor(n / 2)] : (numValues[n / 2 - 1] + numValues[n / 2]) / 2;
    }

    // Standard deviation
    const variance = n > 1 ? numValues.reduce((acc, v) => acc + Math.pow(v - mean, 2), 0) / (n - 1) : 0;
    const std = Math.sqrt(variance);
    const range = max - min;

    // Populate Right Details Panel
    if (detailsPanel) {
      detailsPanel.innerHTML = `
        <div class="chart-stats-mini-grid">
          <div class="chart-mini-stat-card">
            <span class="mini-stat-label"><i class="fa-solid fa-calculator"></i> Mean (Rata-rata)</span>
            <span class="mini-stat-value">${mean >= 1000 ? mean.toLocaleString('id-ID', { maximumFractionDigits: 2 }) : mean.toFixed(2)}</span>
          </div>
          <div class="chart-mini-stat-card">
            <span class="mini-stat-label"><i class="fa-solid fa-arrows-split-up-and-left"></i> Median (Nilai Tengah)</span>
            <span class="mini-stat-value">${median >= 1000 ? median.toLocaleString('id-ID', { maximumFractionDigits: 2 }) : median.toFixed(2)}</span>
          </div>
          <div class="chart-mini-stat-card">
            <span class="mini-stat-label"><i class="fa-solid fa-wave-square"></i> Standar Deviasi (s)</span>
            <span class="mini-stat-value">${std.toFixed(2)}</span>
          </div>
          <div class="chart-mini-stat-card">
            <span class="mini-stat-label"><i class="fa-solid fa-arrow-down-short-wide"></i> Minimum</span>
            <span class="mini-stat-value">${min >= 1000 ? min.toLocaleString('id-ID', { maximumFractionDigits: 2 }) : min.toFixed(2)}</span>
          </div>
          <div class="chart-mini-stat-card">
            <span class="mini-stat-label"><i class="fa-solid fa-arrow-up-wide-short"></i> Maksimum</span>
            <span class="mini-stat-value">${max >= 1000 ? max.toLocaleString('id-ID', { maximumFractionDigits: 2 }) : max.toFixed(2)}</span>
          </div>
          <div class="chart-mini-stat-card">
            <span class="mini-stat-label"><i class="fa-solid fa-arrows-left-right"></i> Rentang (Range)</span>
            <span class="mini-stat-value">${range >= 1000 ? range.toLocaleString('id-ID', { maximumFractionDigits: 2 }) : range.toFixed(2)}</span>
          </div>
        </div>

        <div class="chart-summary-note">
          <i class="fa-solid fa-circle-info" style="color: var(--accent-cyan);"></i>
          <span>Data kuantitatif dengan <strong>N = ${n}</strong> observasi. Nilai berkisar dari <strong>${min.toLocaleString('id-ID')}</strong> sampai <strong>${max.toLocaleString('id-ID')}</strong>.</span>
        </div>
      `;
    }

    // Build histogram bins
    const binCount = Math.min(8, Math.max(4, Math.floor(Math.sqrt(numValues.length))));
    const step = (max - min) / binCount || 1;

    const labels = [];
    const counts = new Array(binCount).fill(0);

    for (let i = 0; i < binCount; i++) {
      const binStart = min + i * step;
      const binEnd = min + (i + 1) * step;
      const formatNum = (val) => val >= 10000 ? (val / 1000).toFixed(0) + 'k' : val.toFixed(1);
      labels.push(`${formatNum(binStart)} - ${formatNum(binEnd)}`);
    }

    numValues.forEach(v => {
      let idx = Math.floor((v - min) / step);
      if (idx >= binCount) idx = binCount - 1;
      if (idx >= 0) counts[idx]++;
    });

    const ctx = canvas.getContext('2d');
    activeChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: `Frekuensi: ${colName}`,
          data: counts,
          backgroundColor: 'rgba(99, 102, 241, 0.75)',
          hoverBackgroundColor: 'rgba(129, 140, 248, 0.95)',
          borderColor: '#818cf8',
          borderWidth: 1.5,
          borderRadius: 5,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 1.22,
        plugins: {
          legend: { display: false },
          title: {
            display: true,
            text: `Histogram: ${colName}`,
            color: '#cbd5e1',
            font: { family: 'Inter', size: 12, weight: '600' },
            padding: { bottom: 4 }
          },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.95)',
            titleFont: { family: 'Inter', size: 11, weight: '700' },
            bodyFont: { family: 'Inter', size: 11 },
            padding: 8,
            borderColor: 'rgba(255, 255, 255, 0.1)',
            borderWidth: 1,
            displayColors: false,
            callbacks: {
              label: (context) => `Jumlah: ${context.parsed.y} (${((context.parsed.y / totalN) * 100).toFixed(1)}%)`
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#94a3b8', font: { size: 9.5 } }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#94a3b8', stepSize: 1, font: { size: 9.5 } }
          }
        }
      }
    });

  } else {
    // -------------------------------------------------------------------------
    // CATEGORICAL COLUMN: PIE / DOUGHNUT & CATEGORY BREAKDOWN TABLE
    // -------------------------------------------------------------------------
    if (typeBadge) {
      typeBadge.className = 'col-type-pill pill-categorical';
      typeBadge.innerHTML = '<i class="fa-solid fa-shapes"></i> Kategorik (Kualitatif)';
    }
    if (iconBadge) {
      iconBadge.innerHTML = '<i class="fa-solid fa-chart-pie"></i>';
      iconBadge.style.background = 'linear-gradient(135deg, #ec4899, #f43f5e)';
    }

    const freqMap = {};
    rawValues.forEach(v => {
      const key = String(v).trim();
      freqMap[key] = (freqMap[key] || 0) + 1;
    });

    // Sort categories descending by frequency
    const sortedEntries = Object.entries(freqMap).sort((a, b) => b[1] - a[1]);
    const labels = sortedEntries.map(e => e[0]);
    const counts = sortedEntries.map(e => e[1]);
    const uniqueCount = labels.length;

    // Palette with vibrant harmonious contrast
    const palette = [
      '#6366f1', '#10b981', '#f59e0b', '#ec4899', '#06b6d4',
      '#8b5cf6', '#3b82f6', '#14b8a6', '#f97316', '#a855f7',
      '#64748b', '#e11d48', '#84cc16', '#0284c7', '#d97706'
    ];

    const chartColors = labels.map((_, idx) => palette[idx % palette.length]);
    const dominantCategory = sortedEntries.length > 0 ? sortedEntries[0] : ['-', 0];
    const dominantPct = totalN > 0 ? ((dominantCategory[1] / totalN) * 100).toFixed(1) : '0';

    // Populate Right Details Panel
    if (detailsPanel) {
      const breakdownRows = sortedEntries.map(([catName, count], idx) => {
        const pct = totalN > 0 ? ((count / totalN) * 100).toFixed(1) : '0.0';
        const color = chartColors[idx];
        return `
          <div class="cat-dist-item">
            <div class="cat-item-left">
              <span class="cat-color-dot" style="background: ${color}; box-shadow: 0 0 6px ${color}88;"></span>
              <span class="cat-name-label" title="${catName}">${catName}</span>
            </div>
            <div class="cat-item-bar-col">
              <div class="cat-bar-track">
                <div class="cat-bar-fill" style="width: ${pct}%; background: ${color};"></div>
              </div>
            </div>
            <div class="cat-item-right">
              <span class="cat-count-badge">${count} <small>(${pct}%)</small></span>
            </div>
          </div>
        `;
      }).join('');

      detailsPanel.innerHTML = `
        <div class="chart-stats-mini-grid" style="grid-template-columns: repeat(3, 1fr); margin-bottom: 10px;">
          <div class="chart-mini-stat-card">
            <span class="mini-stat-label"><i class="fa-solid fa-database"></i> Total Data (N)</span>
            <span class="mini-stat-value">${totalN}</span>
          </div>
          <div class="chart-mini-stat-card">
            <span class="mini-stat-label"><i class="fa-solid fa-layer-group"></i> Kategori (K)</span>
            <span class="mini-stat-value">${uniqueCount}</span>
          </div>
          <div class="chart-mini-stat-card">
            <span class="mini-stat-label"><i class="fa-solid fa-crown" style="color: var(--accent-amber);"></i> Modus (Dominan)</span>
            <span class="mini-stat-value" style="font-size: 12.5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${dominantCategory[0]}">
              ${dominantCategory[0]} <small>(${dominantPct}%)</small>
            </span>
          </div>
        </div>

        <div class="cat-dist-header">
          <span><i class="fa-solid fa-list-check"></i> Rincian Proporsi Kategori</span>
          <span style="font-size: 11px; color: var(--text-muted);">Frekuensi &amp; Rasio</span>
        </div>
        <div class="cat-dist-list">
          ${breakdownRows}
        </div>
      `;
    }

    // Render Doughnut Chart with fixed aspect ratio to ensure it stays in bounds
    const ctx = canvas.getContext('2d');
    activeChartInstance = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: counts,
          backgroundColor: chartColors,
          borderColor: '#0f172a',
          borderWidth: 2,
          hoverOffset: 6,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 1.12,
        cutout: '58%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#94a3b8',
              font: { family: 'Inter', size: 10.5, weight: '500' },
              boxWidth: 8,
              boxHeight: 8,
              padding: 6,
              usePointStyle: true,
              pointStyle: 'circle'
            }
          },
          title: {
            display: true,
            text: `Proporsi: ${colName}`,
            color: '#cbd5e1',
            font: { family: 'Inter', size: 12, weight: '600' },
            padding: { bottom: 4 }
          },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.95)',
            titleFont: { family: 'Inter', size: 11, weight: '700' },
            bodyFont: { family: 'Inter', size: 11 },
            padding: 8,
            borderColor: 'rgba(255, 255, 255, 0.1)',
            borderWidth: 1,
            callbacks: {
              label: (context) => {
                const val = context.parsed;
                const pct = totalN > 0 ? ((val / totalN) * 100).toFixed(1) : 0;
                return ` ${context.label}: ${val} (${pct}%)`;
              }
            }
          }
        }
      }
    });
  }
}
