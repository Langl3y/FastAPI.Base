import { useState } from 'react';
import {
  Box,
  Paper,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Chip,
  CircularProgress,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useTasks } from '../hooks/useTasks';
import TaskDialog from '../components/TaskDialog';
import { Task } from '../types/api';

export default function Tasks() {
  const { tasks, isLoading, createTask, updateTask, deleteTask } = useTasks();
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | undefined>();

  const handleCreateTask = (task: Partial<Task>) => {
    createTask(task as Omit<Task, 'id'>);
  };

  const handleUpdateTask = (task: Partial<Task>) => {
    if (selectedTask?.id) {
      updateTask({ ...task, id: selectedTask.id });
    }
  };

  const handleEdit = (task: Task) => {
    setSelectedTask(task);
    setOpenDialog(true);
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      deleteTask(id);
    }
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedTask(undefined);
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <>
      <Box display="flex" justifyContent="flex-end" mb={2}>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          Create Task
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Due Date</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tasks.map((task: Task) => (
              <TableRow key={task.id}>
                <TableCell>{task.title}</TableCell>
                <TableCell>{task.description}</TableCell>
                <TableCell>
                  {task.due_date && new Date(task.due_date).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Chip
                    label={task.status}
                    color={task.status === 'Completed' ? 'success' : 'warning'}
                  />
                </TableCell>
                <TableCell>
                  <IconButton onClick={() => handleEdit(task)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton onClick={() => task.id && handleDelete(task.id)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <TaskDialog
        open={openDialog}
        onClose={handleCloseDialog}
        onSubmit={selectedTask ? handleUpdateTask : handleCreateTask}
        task={selectedTask}
      />
    </>
  );
}