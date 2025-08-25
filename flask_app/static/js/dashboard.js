// HUIT Student Dashboard - Main JavaScript File

class DashboardApp {
    constructor() {
        this.currentPage = window.location.pathname;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeComponents();
        this.loadInitialData();
    }

    setupEventListeners() {
        // Global search
        const globalSearch = document.getElementById('globalSearch');
        if (globalSearch) {
            globalSearch.addEventListener('input', this.handleGlobalSearch.bind(this));
        }

        // File upload handling
        this.setupFileUpload();

        // Mobile menu toggle
        this.setupMobileMenu();

        // Chart interactions
        this.setupChartInteractions();
    }

    setupFileUpload() {
        const fileUpload = document.querySelector('.file-upload');
        const fileInput = document.querySelector('#fileInput');

        if (fileUpload && fileInput) {
            // Drag and drop
            fileUpload.addEventListener('dragover', (e) => {
                e.preventDefault();
                fileUpload.classList.add('drag-over');
            });

            fileUpload.addEventListener('dragleave', () => {
                fileUpload.classList.remove('drag-over');
            });

            fileUpload.addEventListener('drop', (e) => {
                e.preventDefault();
                fileUpload.classList.remove('drag-over');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.handleFileUpload(files[0]);
                }
            });

            // Click to upload
            fileUpload.addEventListener('click', () => {
                fileInput.click();
            });

            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    this.handleFileUpload(e.target.files[0]);
                }
            });
        }
    }

    setupMobileMenu() {
        const menuToggle = document.querySelector('.menu-toggle');
        const sidebar = document.querySelector('.sidebar');

        if (menuToggle && sidebar) {
            menuToggle.addEventListener('click', () => {
                sidebar.classList.toggle('open');
            });
        }
    }

    setupChartInteractions() {
        // Chart click handlers will be added here
    }

    async handleFileUpload(file) {
        const formData = new FormData();
        formData.append('file', file);

        this.showLoading();

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                this.showAlert('success', result.message);
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                this.showAlert('error', result.error);
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.showAlert('error', 'Có lỗi xảy ra khi tải file');
        } finally {
            this.hideLoading();
        }
    }

    async handleGlobalSearch(event) {
        const query = event.target.value.trim();
        
        if (query.length < 2) return;

        try {
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            if (response.ok) {
                // Handle search results display
                console.log('Search results loaded');
            }
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    initializeComponents() {
        // Initialize charts if on dashboard page
        if (this.currentPage === '/' || this.currentPage.includes('dashboard')) {
            this.initializeDashboardCharts();
        }

        // Initialize data tables
        this.initializeDataTables();

        // Initialize form validation
        this.initializeFormValidation();
    }

    async loadInitialData() {
        try {
            // Load dashboard data
            await this.loadDashboardData();
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    async loadDashboardData() {
        try {
            const response = await fetch('/api/dashboard-data');
            if (response.ok) {
                const data = await response.json();
                this.updateDashboardMetrics(data);
            }
        } catch (error) {
            console.error('Error loading dashboard data:', error);
        }
    }

    updateDashboardMetrics(data) {
        // Update metric cards
        const metrics = {
            'totalStudents': data.total_students || 0,
            'totalClasses': data.total_classes || 0,
            'averageScore': (data.average_score || 0).toFixed(1),
            'passRate': (data.pass_rate || 0).toFixed(1) + '%'
        };

        Object.keys(metrics).forEach(key => {
            const element = document.getElementById(key);
            if (element) {
                element.textContent = metrics[key];
            }
        });
    }

    async initializeDashboardCharts() {
        try {
            // Class Distribution Chart
            await this.createClassDistributionChart();
            
            // Score Distribution Chart
            await this.createScoreDistributionChart();
            
        } catch (error) {
            console.error('Error initializing charts:', error);
        }
    }

    async createClassDistributionChart() {
        const canvas = document.getElementById('classDistributionChart');
        if (!canvas) return;

        try {
            const response = await fetch('/api/chart/class_distribution');
            if (response.ok) {
                const data = await response.json();
                
                new Chart(canvas, {
                    type: 'doughnut',
                    data: {
                        labels: data.labels || [],
                        datasets: [{
                            data: data.values || [],
                            backgroundColor: [
                                '#3b82f6', '#10b981', '#f59e0b', '#ef4444',
                                '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'
                            ],
                            borderWidth: 2,
                            borderColor: '#ffffff'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    padding: 20,
                                    usePointStyle: true
                                }
                            }
                        }
                    }
                });
            }
        } catch (error) {
            console.error('Error creating class distribution chart:', error);
        }
    }

    async createScoreDistributionChart() {
        const canvas = document.getElementById('scoreDistributionChart');
        if (!canvas) return;

        try {
            const response = await fetch('/api/chart/score_histogram');
            if (response.ok) {
                const data = await response.json();
                
                if (data.labels && data.counts) {
                    new Chart(canvas, {
                        type: 'bar',
                        data: {
                            labels: data.labels,
                            datasets: [{
                                label: 'Số sinh viên',
                                data: data.counts,
                                backgroundColor: [
                                    '#ef4444', // Kém - Red
                                    '#f97316', // Yếu - Orange
                                    '#f59e0b', // TB- - Amber
                                    '#10b981', // TB - Green
                                    '#3b82f6', // Khá - Blue
                                    '#8b5cf6'  // Giỏi - Purple
                                ],
                                borderColor: [
                                    '#dc2626', '#ea580c', '#d97706', 
                                    '#059669', '#2563eb', '#7c3aed'
                                ],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    ticks: {
                                        stepSize: 1
                                    }
                                }
                            },
                            plugins: {
                                legend: {
                                    display: false
                                },
                                tooltip: {
                                    callbacks: {
                                        label: function(context) {
                                            return `${context.parsed.y} sinh viên`;
                                        }
                                    }
                                }
                            }
                        }
                    });
                } else {
                    console.warn('No score data available for chart');
                }
            }
        } catch (error) {
            console.error('Error creating score distribution chart:', error);
        }
    }

    initializeDataTables() {
        // Add sorting, filtering functionality to tables
        const tables = document.querySelectorAll('.data-table');
        tables.forEach(table => {
            this.enhanceTable(table);
        });
    }

    enhanceTable(table) {
        const headers = table.querySelectorAll('th[data-sortable]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                this.sortTable(table, header);
            });
        });
    }

    sortTable(table, header) {
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const columnIndex = Array.from(header.parentNode.children).indexOf(header);
        const isAscending = header.dataset.sort !== 'asc';

        rows.sort((a, b) => {
            const aValue = a.cells[columnIndex].textContent.trim();
            const bValue = b.cells[columnIndex].textContent.trim();
            
            const aNum = parseFloat(aValue);
            const bNum = parseFloat(bValue);
            
            if (!isNaN(aNum) && !isNaN(bNum)) {
                return isAscending ? aNum - bNum : bNum - aNum;
            }
            
            return isAscending ? 
                aValue.localeCompare(bValue) : 
                bValue.localeCompare(aValue);
        });

        // Clear and re-append sorted rows
        tbody.innerHTML = '';
        rows.forEach(row => tbody.appendChild(row));

        // Update sort indicator
        header.dataset.sort = isAscending ? 'asc' : 'desc';
        
        // Remove sort indicators from other headers
        table.querySelectorAll('th').forEach(th => {
            if (th !== header) {
                th.removeAttribute('data-sort');
            }
        });
    }

    initializeFormValidation() {
        const forms = document.querySelectorAll('form[data-validate]');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
    }

    validateForm(form) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                this.showFieldError(field, 'Trường này là bắt buộc');
                isValid = false;
            } else {
                this.clearFieldError(field);
            }
        });

        return isValid;
    }

    showFieldError(field, message) {
        this.clearFieldError(field);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;
        errorDiv.style.color = '#ef4444';
        errorDiv.style.fontSize = '0.875rem';
        errorDiv.style.marginTop = '0.25rem';
        
        field.parentNode.appendChild(errorDiv);
        field.style.borderColor = '#ef4444';
    }

    clearFieldError(field) {
        const errorDiv = field.parentNode.querySelector('.field-error');
        if (errorDiv) {
            errorDiv.remove();
        }
        field.style.borderColor = '';
    }

    showLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = 'flex';
        }
    }

    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }

    showAlert(type, message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = `
            <i data-lucide="${type === 'success' ? 'check-circle' : type === 'error' ? 'x-circle' : 'info'}" class="alert-icon"></i>
            ${message}
        `;

        const container = document.querySelector('.content-wrapper');
        container.insertBefore(alertDiv, container.firstChild);

        // Initialize icon
        lucide.createIcons();

        // Auto remove after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    // Utility methods
    formatNumber(num) {
        return new Intl.NumberFormat('vi-VN').format(num);
    }

    formatDate(date) {
        return new Date(date).toLocaleDateString('vi-VN');
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Statistics App for detailed statistics page
class StatisticsApp {
    constructor() {
        this.currentPage = window.location.pathname;
    }

    async init() {
        if (this.currentPage.includes('statistics')) {
            await this.loadDetailedStatistics();
            await this.loadClassAnalysis();
            await this.loadTopStudents();
            await this.loadRecommendations();
            this.setupEventListeners();
        }
    }

    setupEventListeners() {
        const classFilter = document.getElementById('classFilter');
        if (classFilter) {
            classFilter.addEventListener('change', this.handleClassFilter.bind(this));
        }
    }

    async loadDetailedStatistics() {
        try {
            const response = await fetch('/api/statistics/detailed');
            if (response.ok) {
                const data = await response.json();
                this.updateDetailedMetrics(data);
                this.createDetailedCharts(data);
                this.updateAdvancedStats(data);
            }
        } catch (error) {
            console.error('Error loading detailed statistics:', error);
        }
    }

    updateDetailedMetrics(data) {
        const elements = {
            'totalStudentsDetail': data.basic_stats?.total_students || 0,
            'averageGPA': (data.basic_stats?.mean || 0).toFixed(2),
            'passRateDetail': (data.advanced_stats?.pass_rate || 0).toFixed(1) + '%',
            'excellentCount': Math.round((data.basic_stats?.total_students || 0) * (data.advanced_stats?.excellent_rate || 0) / 100)
        };

        Object.keys(elements).forEach(key => {
            const element = document.getElementById(key);
            if (element) {
                element.textContent = elements[key];
            }
        });
    }

    createDetailedCharts(data) {
        this.createDetailedScoreChart(data);
        this.createTrendChart(data);
    }

    createDetailedScoreChart(data) {
        const canvas = document.getElementById('detailedScoreChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.grade_distribution?.map(item => item.label) || [],
                datasets: [{
                    label: 'Số sinh viên',
                    data: data.grade_distribution?.map(item => item.count) || [],
                    backgroundColor: [
                        '#ef4444', '#f97316', '#f59e0b', 
                        '#10b981', '#3b82f6', '#8b5cf6'
                    ],
                    borderColor: [
                        '#dc2626', '#ea580c', '#d97706', 
                        '#059669', '#2563eb', '#7c3aed'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            afterLabel: function(context) {
                                const percentage = data.grade_distribution?.[context.dataIndex]?.percentage || 0;
                                return `${percentage.toFixed(1)}% của tổng số`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });

        // Update chart stats
        this.updateChartStats(data);
    }

    updateChartStats(data) {
        const statsContainer = document.getElementById('scoreStats');
        if (!statsContainer || !data.basic_stats) return;

        statsContainer.innerHTML = `
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-label">Trung bình:</span>
                    <span class="stat-value">${data.basic_stats.mean.toFixed(2)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Trung vị:</span>
                    <span class="stat-value">${data.basic_stats.median.toFixed(2)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Độ lệch chuẩn:</span>
                    <span class="stat-value">${data.basic_stats.std_dev.toFixed(2)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Phạm vi:</span>
                    <span class="stat-value">${data.basic_stats.range.toFixed(2)}</span>
                </div>
            </div>
        `;
    }

    createTrendChart(data) {
        const canvas = document.getElementById('trendChart');
        if (!canvas) return;

        // Create sample trend data for demonstration
        const months = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6'];
        const baseScore = data.basic_stats?.mean || 6.0;
        const trendData = months.map((month, index) => {
            return baseScore + (Math.random() - 0.5) * 2 + (index * 0.1);
        });

        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: months,
                datasets: [{
                    label: 'Điểm trung bình',
                    data: trendData,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 0,
                        max: 10
                    }
                }
            }
        });
    }

    updateAdvancedStats(data) {
        const elements = {
            'standardDeviation': data.basic_stats?.std_dev?.toFixed(2) || '0',
            'coefficientVariation': data.advanced_stats?.coefficient_variation?.toFixed(1) + '%' || '0%',
            'skewness': data.advanced_stats?.skewness?.toFixed(3) || '0'
        };

        Object.keys(elements).forEach(key => {
            const element = document.getElementById(key);
            if (element) {
                element.textContent = elements[key];
            }
        });

        // Update quartile analysis
        this.updateQuartileAnalysis(data.quartiles);
        this.updateOutlierAnalysis(data.advanced_stats);
    }

    updateQuartileAnalysis(quartiles) {
        const container = document.getElementById('quartileAnalysis');
        if (!container || !quartiles) return;

        container.innerHTML = `
            <div class="quartile-item">
                <span>Q1 (25%):</span> <strong>${quartiles.q1?.toFixed(2)}</strong>
            </div>
            <div class="quartile-item">
                <span>Q2 (50% - Trung vị):</span> <strong>${quartiles.q2?.toFixed(2)}</strong>
            </div>
            <div class="quartile-item">
                <span>Q3 (75%):</span> <strong>${quartiles.q3?.toFixed(2)}</strong>
            </div>
            <div class="quartile-item">
                <span>IQR:</span> <strong>${quartiles.iqr?.toFixed(2)}</strong>
            </div>
        `;
    }

    updateOutlierAnalysis(stats) {
        const container = document.getElementById('outlierAnalysis');
        if (!container || !stats) return;

        const outlierClass = stats.outlier_percentage > 5 ? 'warning' : 'normal';
        
        container.innerHTML = `
            <div class="outlier-item">
                <span>Số lượng outliers:</span> 
                <strong class="${outlierClass}">${stats.outlier_count || 0}</strong>
            </div>
            <div class="outlier-item">
                <span>Tỷ lệ outliers:</span> 
                <strong class="${outlierClass}">${stats.outlier_percentage?.toFixed(1) || 0}%</strong>
            </div>
            <div class="outlier-description">
                ${stats.outlier_percentage > 5 ? 
                    'Có nhiều điểm bất thường, cần kiểm tra dữ liệu.' : 
                    'Dữ liệu khá đồng đều, ít điểm bất thường.'}
            </div>
        `;
    }

    async loadClassAnalysis() {
        try {
            const response = await fetch('/api/statistics/class-analysis');
            if (response.ok) {
                const data = await response.json();
                this.updateClassFilter(data);
                this.createClassPerformanceChart(data);
                this.updateClassMetrics(data);
            }
        } catch (error) {
            console.error('Error loading class analysis:', error);
        }
    }

    updateClassFilter(classData) {
        const classFilter = document.getElementById('classFilter');
        if (!classFilter) return;

        classFilter.innerHTML = '<option value="">Tất cả lớp</option>';
        classData.forEach(cls => {
            const option = document.createElement('option');
            option.value = cls.class_name;
            option.textContent = `${cls.class_name} (${cls.student_count} SV)`;
            classFilter.appendChild(option);
        });
    }

    createClassPerformanceChart(classData) {
        const canvas = document.getElementById('classPerformanceChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: classData.map(cls => cls.class_name),
                datasets: [{
                    label: 'Điểm trung bình',
                    data: classData.map(cls => cls.mean),
                    backgroundColor: '#3b82f6',
                    borderColor: '#2563eb',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 10
                    }
                }
            }
        });
    }

    updateClassMetrics(classData) {
        const container = document.getElementById('classMetrics');
        if (!container || !classData.length) return;

        const bestClass = classData[0];
        const worstClass = classData[classData.length - 1];

        container.innerHTML = `
            <div class="class-metric">
                <h5><i data-lucide="trophy" style="width: 16px; height: 16px; color: #f59e0b; margin-right: 0.5rem;"></i>Lớp xuất sắc nhất</h5>
                <p><strong>${bestClass.class_name}</strong></p>
                <p>Điểm TB: <strong>${bestClass.mean.toFixed(2)}</strong></p>
                <p>Tỷ lệ qua môn: <strong>${bestClass.pass_rate.toFixed(1)}%</strong></p>
            </div>
            <div class="class-metric">
                <h5><i data-lucide="alert-triangle" style="width: 16px; height: 16px; color: #ef4444; margin-right: 0.5rem;"></i>Lớp cần hỗ trợ</h5>
                <p><strong>${worstClass.class_name}</strong></p>
                <p>Điểm TB: <strong>${worstClass.mean.toFixed(2)}</strong></p>
                <p>Tỷ lệ qua môn: <strong>${worstClass.pass_rate.toFixed(1)}%</strong></p>
            </div>
            <div class="class-metric">
                <h5><i data-lucide="bar-chart-3" style="width: 16px; height: 16px; color: #3b82f6; margin-right: 0.5rem;"></i>Tổng quan</h5>
                <p>Số lớp: <strong>${classData.length}</strong></p>
                <p>Chênh lệch: <strong>${(bestClass.mean - worstClass.mean).toFixed(2)} điểm</strong></p>
            </div>
        `;
        
        // Re-initialize Lucide icons for the new content
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    async loadTopStudents() {
        try {
            const response = await fetch('/api/statistics/top-students');
            if (response.ok) {
                const data = await response.json();
                this.updateTopStudents(data.top_students);
                this.updateLowPerformers(data.low_performers);
            }
        } catch (error) {
            console.error('Error loading top students:', error);
        }
    }

    updateTopStudents(topStudents) {
        const container = document.getElementById('topStudents');
        if (!container) return;

        container.innerHTML = topStudents.map(student => `
            <div class="ranking-item">
                <div class="ranking-number ${this.getRankingClass(student.rank)}">
                    ${student.rank}
                </div>
                <div class="ranking-info">
                    <div class="student-name">${student.name}</div>
                    <div class="student-class">${student.class}</div>
                </div>
                <div class="ranking-score">
                    ${student.score.toFixed(2)}
                </div>
            </div>
        `).join('');
    }

    updateLowPerformers(lowPerformers) {
        const container = document.getElementById('lowPerformers');
        if (!container) return;

        if (lowPerformers.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 2rem; color: #10b981;">
                    <i data-lucide="check-circle" style="width: 48px; height: 48px; margin-bottom: 1rem; color: #10b981;"></i>
                    <p>Tất cả sinh viên đều đạt điểm qua môn!</p>
                </div>
            `;
            // Re-initialize Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
            return;
        }

        container.innerHTML = lowPerformers.map(student => `
            <div class="ranking-item">
                <div class="ranking-number default">
                    ${student.rank}
                </div>
                <div class="ranking-info">
                    <div class="student-name">${student.name}</div>
                    <div class="student-class">${student.class}</div>
                </div>
                <div class="ranking-score" style="color: #ef4444;">
                    ${student.score.toFixed(2)}
                </div>
            </div>
        `).join('');
    }

    getRankingClass(rank) {
        if (rank === 1) return 'gold';
        if (rank === 2) return 'silver';
        if (rank === 3) return 'bronze';
        return 'default';
    }

    async loadRecommendations() {
        try {
            const response = await fetch('/api/statistics/recommendations');
            if (response.ok) {
                const data = await response.json();
                this.updateRecommendations(data.recommendations);
            }
        } catch (error) {
            console.error('Error loading recommendations:', error);
        }
    }

    updateRecommendations(recommendations) {
        const container = document.getElementById('recommendations');
        if (!container) return;

        if (recommendations.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 2rem; color: #10b981;">
                    <i data-lucide="thumbs-up" style="width: 48px; height: 48px; margin-bottom: 1rem; color: #10b981;"></i>
                    <p>Tất cả các chỉ số đều ở mức tốt!</p>
                </div>
            `;
            // Re-initialize Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
            return;
        }

        container.innerHTML = recommendations.map(rec => `
            <div class="recommendation-item">
                <div class="recommendation-icon">
                    ${this.getRecommendationIcon(rec.type)}
                </div>
                <div class="recommendation-content">
                    <h5>${rec.title}</h5>
                    <p>${rec.message}</p>
                </div>
            </div>
        `).join('');
        
        // Re-initialize Lucide icons for the new content
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    getRecommendationIcon(type) {
        const icons = {
            'error': '<i data-lucide="alert-circle" style="color: #ef4444; width: 24px; height: 24px;"></i>',
            'warning': '<i data-lucide="alert-triangle" style="color: #f59e0b; width: 24px; height: 24px;"></i>',
            'info': '<i data-lucide="info" style="color: #3b82f6; width: 24px; height: 24px;"></i>',
            'success': '<i data-lucide="check-circle" style="color: #10b981; width: 24px; height: 24px;"></i>'
        };
        return icons[type] || icons['info'];
    }

    handleClassFilter(event) {
        const selectedClass = event.target.value;
        // Implement class filtering logic here
        console.log('Filter by class:', selectedClass);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboardApp = new DashboardApp();
    window.statisticsApp = new StatisticsApp();
    
    // Initialize statistics app
    window.statisticsApp.init();
});

// Export for use in other modules
window.DashboardApp = DashboardApp;
window.StatisticsApp = StatisticsApp;
