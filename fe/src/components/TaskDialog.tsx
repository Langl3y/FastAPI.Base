import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, MenuItem } from '@mui/material';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { Task, TaskStatus } from '../types/api';

const validationSchema = yup.object({
  title: yup.string().required('Title is required'),
  description: yup.string(),
  due_date: yup.date(),
  status: yup.string().oneOf(['Pending', 'Completed']).required('Status is required'),
});

interface TaskDialogProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (task: Partial<Task>) => void;
  task?: Task;
}

export default function TaskDialog({ open, onClose, onSubmit, task }: TaskDialogProps) {
  const formik = useFormik({
    initialValues: {
      title: task?.title || '',
      description: task?.description || '',
      due_date: task?.due_date ? new Date(task.due_date).toISOString().split('T')[0] : '',
      status: task?.status || 'Pending',
      user_id: task?.user_id || 1, // You might want to get this from your auth context
    },
    validationSchema,
    onSubmit: (values) => {
      onSubmit({
        ...values,
        status: values.status as TaskStatus
      });
      onClose();
    },
    enableReinitialize: true,
  });

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <form onSubmit={formik.handleSubmit}>
        <DialogTitle>{task ? 'Edit Task' : 'Create Task'}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            margin="normal"
            name="title"
            label="Title"
            value={formik.values.title}
            onChange={formik.handleChange}
            error={formik.touched.title && Boolean(formik.errors.title)}
            helperText={formik.touched.title && formik.errors.title}
          />
          <TextField
            fullWidth
            margin="normal"
            name="description"
            label="Description"
            multiline
            rows={4}
            value={formik.values.description}
            onChange={formik.handleChange}
          />
          <TextField
            fullWidth
            margin="normal"
            name="due_date"
            label="Due Date"
            type="date"
            value={formik.values.due_date}
            onChange={formik.handleChange}
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            fullWidth
            margin="normal"
            name="status"
            label="Status"
            select
            value={formik.values.status}
            onChange={formik.handleChange}
          >
            <MenuItem value="Pending">Pending</MenuItem>
            <MenuItem value="Completed">Completed</MenuItem>
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained">
            {task ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}