/**
 * Advanced Task Manager with async operations
 */

class TaskManager {
    constructor() {
        this.tasks = [];
        this.listeners = new Set();
    }

    /**
     * Add a new task
     * @param {string} title - Task title
     * @param {number} priority - Priority (1-5)
     * @returns {Object} Created task
     */
    addTask(title, priority = 3) {
        if (!title || title.trim() === '') {
            throw new Error('Task title is required');
        }

        if (priority < 1 || priority > 5) {
            throw new Error('Priority must be between 1 and 5');
        }

        const task = {
            id: Date.now(),
            title: title.trim(),
            priority,
            completed: false,
            createdAt: new Date(),
            updatedAt: new Date()
        };

        this.tasks.push(task);
        this._notifyListeners('taskAdded', task);
        
        return task;
    }

    /**
     * Complete a task
     * @param {number} taskId - Task ID
     * @returns {boolean} Success status
     */
    completeTask(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        
        if (!task) {
            console.warn(`Task ${taskId} not found`);
            return false;
        }

        task.completed = true;
        task.updatedAt = new Date();
        
        this._notifyListeners('taskCompleted', task);
        
        return true;
    }

    /**
     * Get tasks filtered by completion status
     * @param {boolean} completed - Filter by completion
     * @returns {Array} Filtered tasks
     */
    getTasks(completed = null) {
        if (completed === null) {
            return [...this.tasks];
        }
        
        return this.tasks.filter(task => task.completed === completed);
    }

    /**
     * Get tasks sorted by priority
     * @returns {Array} Sorted tasks
     */
    getTasksByPriority() {
        return [...this.tasks].sort((a, b) => b.priority - a.priority);
    }

    /**
     * Simulate async task processing
     * @param {number} taskId - Task ID
     * @returns {Promise} Processing result
     */
    async processTask(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        
        if (!task) {
            return Promise.reject(new Error('Task not found'));
        }

        if (task.completed) {
            return Promise.resolve({
                message: 'Task already completed',
                task
            });
        }

        return new Promise((resolve, reject) => {
            setTimeout(() => {
                try {
                    this.completeTask(taskId);
                    resolve({
                        message: 'Task processed successfully',
                        task
                    });
                } catch (error) {
                    reject(error);
                }
            }, 2000);
        });
    }

    /**
     * Add change listener
     * @param {Function} listener - Callback function
     */
    addListener(listener) {
        this.listeners.add(listener);
    }

    /**
     * Remove change listener
     * @param {Function} listener - Callback function
     */
    removeListener(listener) {
        this.listeners.delete(listener);
    }

    /**
     * Notify all listeners
     * @private
     */
    _notifyListeners(event, data) {
        this.listeners.forEach(listener => {
            try {
                listener(event, data);
            } catch (error) {
                console.error('Listener error:', error);
            }
        });
    }
}

// Usage example
const manager = new TaskManager();

// Add listeners
manager.addListener((event, task) => {
    console.log(`Event: ${event}`, task);
});

// Add some tasks
try {
    manager.addTask('Implement login feature', 5);
    manager.addTask('Fix navigation bug', 4);
    manager.addTask('Update documentation', 2);
    
    // Process a task
    manager.processTask(manager.tasks[0].id)
        .then(result => console.log('Process result:', result))
        .catch(error => console.error('Process error:', error));
    
    // Get tasks by priority
    const prioritized = manager.getTasksByPriority();
    console.log('Prioritized tasks:', prioritized);
    
} catch (error) {
    console.error('Error:', error.message);
}