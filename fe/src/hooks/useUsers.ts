import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';
import { usersApi } from '../services/api';
import { User } from '../types/api';
import { useNotification } from '../contexts/NotificationContext';

export function useUsers() {
  const queryClient = useQueryClient();
  const { showNotification } = useNotification();

  const { data: users = [], isLoading, error } = useQuery<User[], Error>({
    queryKey: ['users'],
    queryFn: usersApi.getUsers,
    refetchOnWindowFocus: false,
    retry: false
  });

  const createUserMutation = useMutation({
    mutationFn: usersApi.createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      showNotification('User created successfully', 'success');
    },
    onError: (error: Error) => {
      showNotification(error.message || 'Failed to create user', 'error');
    }
  });

  const updateUserMutation = useMutation({
    mutationFn: usersApi.updateUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      showNotification('User updated successfully', 'success');
    },
    onError: (error: Error) => {
      showNotification(error.message || 'Failed to update user', 'error');
    }
  });

  const deleteUserMutation = useMutation({
    mutationFn: usersApi.deleteUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      showNotification('User deleted successfully', 'success');
    },
    onError: (error: Error) => {
      showNotification(error.message || 'Failed to delete user', 'error');
    }
  });

  useEffect(() => {
    if (error) {
      showNotification(error.message || 'Failed to fetch users', 'error');
    }
  }, [error, showNotification]);

  return {
    users,
    isLoading,
    error,
    createUser: createUserMutation.mutateAsync,
    updateUser: updateUserMutation.mutateAsync,
    deleteUser: deleteUserMutation.mutateAsync
  };
}