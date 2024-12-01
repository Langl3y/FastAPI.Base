import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';
import { tasksApi } from '../services/api';
import { Task, TaskStatus } from '../types/api';
import { useNotification } from '../contexts/NotificationContext';

export function useTasks() {
  const queryClient = useQueryClient();
  const { showNotification } = useNotification();

  const { data: tasks = [], isLoading, error } = useQuery<Task[], Error>({
    queryKey: ['tasks'],
    queryFn: tasksApi.getTasks,
    refetchOnWindowFocus: false,
    retry: false
  });

  const createTaskMutation = useMutation({
    mutationFn: tasksApi.createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      showNotification('Task created successfully', 'success');
    },
    onError: (error: Error) => {
      showNotification(error.message || 'Failed to create task', 'error');
    }
  });

  const updateTaskMutation = useMutation({
    mutationFn: tasksApi.updateTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      showNotification('Task updated successfully', 'success');
    },
    onError: (error: Error) => {
      showNotification(error.message || 'Failed to update task', 'error');
    }
  });

  const deleteTaskMutation = useMutation({
    mutationFn: tasksApi.deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      showNotification('Task deleted successfully', 'success');
    },
    onError: (error: Error) => {
      showNotification(error.message || 'Failed to delete task', 'error');
    }
  });

  useEffect(() => {
    if (error) {
      showNotification(error.message || 'Failed to fetch tasks', 'error');
    }
  }, [error, showNotification]);

  return {
    tasks,
    isLoading,
    error,
    createTask: createTaskMutation.mutateAsync,
    updateTask: updateTaskMutation.mutateAsync,
    deleteTask: deleteTaskMutation.mutateAsync,
    TaskStatus
  };
}