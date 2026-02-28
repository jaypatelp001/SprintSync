/**
 * Dashboard — Main view with task list, create modal, and AI suggest.
 */
import { useState, useEffect } from 'react';
import { api } from '../api';
import TaskCard from './TaskCard';
import TaskModal from './TaskModal';

const STATUS_FILTERS = [
    { value: '', label: 'All Tasks' },
    { value: 'todo', label: '📋 To Do' },
    { value: 'in_progress', label: '🔄 In Progress' },
    { value: 'review', label: '👀 Review' },
    { value: 'done', label: '✅ Done' },
];

export default function Dashboard({ user, onLogout }) {
    const [tasks, setTasks] = useState([]);
    const [total, setTotal] = useState(0);
    const [statusFilter, setStatusFilter] = useState('');
    const [showModal, setShowModal] = useState(false);
    const [editingTask, setEditingTask] = useState(null);
    const [loading, setLoading] = useState(true);
    const [dailyPlan, setDailyPlan] = useState(null);
    const [planLoading, setPlanLoading] = useState(false);

    const loadTasks = async () => {
        setLoading(true);
        try {
            const params = {};
            if (statusFilter) params.status = statusFilter;
            const data = await api.listTasks(params);
            setTasks(data.tasks);
            setTotal(data.total);
        } catch (err) {
            console.error('Failed to load tasks:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadTasks();
    }, [statusFilter]);

    const handleCreateTask = () => {
        setEditingTask(null);
        setShowModal(true);
    };

    const handleEditTask = (task) => {
        setEditingTask(task);
        setShowModal(true);
    };

    const handleSaveTask = async (taskData) => {
        try {
            if (editingTask) {
                await api.updateTask(editingTask.id, taskData);
            } else {
                await api.createTask(taskData);
            }
            setShowModal(false);
            loadTasks();
        } catch (err) {
            throw err; // Let the modal handle the error
        }
    };

    const handleStatusChange = async (taskId, newStatus) => {
        try {
            await api.updateTaskStatus(taskId, newStatus);
            loadTasks();
        } catch (err) {
            alert(err.message);
        }
    };

    const handleDeleteTask = async (taskId) => {
        if (!window.confirm('Delete this task?')) return;
        try {
            await api.deleteTask(taskId);
            loadTasks();
        } catch (err) {
            alert(err.message);
        }
    };

    const handleLogTime = async (taskId, minutes) => {
        try {
            await api.logTime(taskId, minutes);
            loadTasks();
        } catch (err) {
            alert(err.message);
        }
    };

    const handleDailyPlan = async () => {
        setPlanLoading(true);
        try {
            const data = await api.aiSuggest('daily_plan');
            setDailyPlan(data.suggestion);
        } catch (err) {
            alert(err.message);
        } finally {
            setPlanLoading(false);
        }
    };

    const statusCounts = {
        todo: tasks.filter(t => t.status === 'todo').length,
        in_progress: tasks.filter(t => t.status === 'in_progress').length,
        review: tasks.filter(t => t.status === 'review').length,
        done: tasks.filter(t => t.status === 'done').length,
    };

    return (
        <div className="dashboard">
            {/* Header */}
            <header className="dashboard-header">
                <div className="header-left">
                    <h1>⚡ SprintSync</h1>
                </div>
                <div className="header-right">
                    <span className="user-badge">
                        {user.is_admin && <span className="admin-tag">ADMIN</span>}
                        {user.username}
                    </span>
                    <button onClick={onLogout} className="btn-ghost">Logout</button>
                </div>
            </header>

            {/* Stats Bar */}
            <div className="stats-bar">
                <div className="stat-item">
                    <span className="stat-value">{total}</span>
                    <span className="stat-label">Total</span>
                </div>
                <div className="stat-item todo">
                    <span className="stat-value">{statusCounts.todo}</span>
                    <span className="stat-label">To Do</span>
                </div>
                <div className="stat-item in-progress">
                    <span className="stat-value">{statusCounts.in_progress}</span>
                    <span className="stat-label">In Progress</span>
                </div>
                <div className="stat-item review">
                    <span className="stat-value">{statusCounts.review}</span>
                    <span className="stat-label">Review</span>
                </div>
                <div className="stat-item done">
                    <span className="stat-value">{statusCounts.done}</span>
                    <span className="stat-label">Done</span>
                </div>
            </div>

            {/* Toolbar */}
            <div className="toolbar">
                <div className="filter-group">
                    {STATUS_FILTERS.map(f => (
                        <button
                            key={f.value}
                            className={`filter-btn ${statusFilter === f.value ? 'active' : ''}`}
                            onClick={() => setStatusFilter(f.value)}
                        >
                            {f.label}
                        </button>
                    ))}
                </div>
                <div className="action-group">
                    <button
                        onClick={handleDailyPlan}
                        className="btn-secondary"
                        disabled={planLoading}
                    >
                        {planLoading ? '⏳' : '🤖'} AI Daily Plan
                    </button>
                    <button onClick={handleCreateTask} className="btn-primary">
                        + New Task
                    </button>
                </div>
            </div>

            {/* AI Daily Plan */}
            {dailyPlan && (
                <div className="daily-plan">
                    <div className="plan-header">
                        <h3>🤖 AI Daily Plan</h3>
                        <button onClick={() => setDailyPlan(null)} className="btn-close">✕</button>
                    </div>
                    <pre className="plan-content">{dailyPlan}</pre>
                </div>
            )}

            {/* Task List */}
            <div className="task-list">
                {loading ? (
                    <div className="loading-tasks">
                        <div className="spinner"></div>
                        <p>Loading tasks...</p>
                    </div>
                ) : tasks.length === 0 ? (
                    <div className="empty-state">
                        <p>No tasks found. Create one to get started!</p>
                    </div>
                ) : (
                    tasks.map(task => (
                        <TaskCard
                            key={task.id}
                            task={task}
                            onEdit={handleEditTask}
                            onStatusChange={handleStatusChange}
                            onDelete={handleDeleteTask}
                            onLogTime={handleLogTime}
                        />
                    ))
                )}
            </div>

            {/* Create/Edit Modal */}
            {showModal && (
                <TaskModal
                    task={editingTask}
                    onSave={handleSaveTask}
                    onClose={() => setShowModal(false)}
                />
            )}
        </div>
    );
}
