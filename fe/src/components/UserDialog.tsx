import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { User } from '../types/api';

const validationSchema = yup.object({
  username: yup.string().required('Username is required'),
  password: yup.string().when('isNew', {
    is: true,
    then: (schema) => schema.required('Password is required'),
    otherwise: (schema) => schema,
  }),
});

interface UserDialogProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (user: Partial<User>) => void;
  user?: User;
}

export default function UserDialog({ open, onClose, onSubmit, user }: UserDialogProps) {
  const formik = useFormik({
    initialValues: {
      username: user?.username || '',
      password: '',
      isNew: !user,
    },
    validationSchema,
    onSubmit: (values) => {
      onSubmit(values);
      onClose();
    },
    enableReinitialize: true,
  });

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <form onSubmit={formik.handleSubmit}>
        <DialogTitle>{user ? 'Edit User' : 'Create User'}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            margin="normal"
            name="username"
            label="Username"
            value={formik.values.username}
            onChange={formik.handleChange}
            error={formik.touched.username && Boolean(formik.errors.username)}
            helperText={formik.touched.username && formik.errors.username}
          />
          <TextField
            fullWidth
            margin="normal"
            name="password"
            label="Password"
            type="password"
            value={formik.values.password}
            onChange={formik.handleChange}
            error={formik.touched.password && Boolean(formik.errors.password)}
            helperText={formik.touched.password && formik.errors.password}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained">
            {user ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}