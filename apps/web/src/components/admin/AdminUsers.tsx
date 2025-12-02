"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Badge } from "../ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../ui/table";
import { Label } from "../ui/label";
import { Checkbox } from "../ui/checkbox";
import { Search, Plus, Edit, Trash2, UserCheck, UserX } from "lucide-react";
import {
  listUsers,
  createUser,
  updateUser,
  deleteUser,
  toggleUserActive,
  UserRead,
  UserCreatePayload,
  UserUpdatePayload,
} from "@/lib/api";

export function AdminUsers() {
  const [users, setUsers] = useState<UserRead[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<UserRead | null>(null);
  const [formData, setFormData] = useState<UserCreatePayload>({
    phone: "",
    email: "",
    first_name: "",
    last_name: "",
    is_admin: false,
    is_super_admin: false,
    is_active: true,
  });

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const data = await listUsers();
      setUsers(data);
    } catch (error) {
      console.error("Failed to load users:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    try {
      await createUser(formData);
      setIsCreateDialogOpen(false);
      resetForm();
      loadUsers();
    } catch (error) {
      console.error("Failed to create user:", error);
      alert("Failed to create user. Please try again.");
    }
  };

  const handleEdit = (user: UserRead) => {
    setSelectedUser(user);
    setFormData({
      phone: user.phone || "",
      email: user.email || "",
      first_name: user.first_name || "",
      last_name: user.last_name || "",
      is_admin: user.is_admin,
      is_super_admin: user.is_super_admin,
      is_active: user.is_active,
    });
    setIsEditDialogOpen(true);
  };

  const handleUpdate = async () => {
    if (!selectedUser) return;
    try {
      const updatePayload: UserUpdatePayload = {
        phone: formData.phone,
        email: formData.email || null,
        first_name: formData.first_name || null,
        last_name: formData.last_name || null,
        is_admin: formData.is_admin,
        is_super_admin: formData.is_super_admin,
        is_active: formData.is_active,
      };
      await updateUser(selectedUser.id, updatePayload);
      setIsEditDialogOpen(false);
      resetForm();
      setSelectedUser(null);
      loadUsers();
    } catch (error) {
      console.error("Failed to update user:", error);
      alert("Failed to update user. Please try again.");
    }
  };

  const handleDelete = async () => {
    if (!selectedUser) return;
    try {
      await deleteUser(selectedUser.id);
      setIsDeleteDialogOpen(false);
      setSelectedUser(null);
      loadUsers();
    } catch (error) {
      console.error("Failed to delete user:", error);
      alert("Failed to delete user. Please try again.");
    }
  };

  const handleToggleActive = async (user: UserRead) => {
    try {
      await toggleUserActive(user.id, !user.is_active);
      loadUsers();
    } catch (error) {
      console.error("Failed to toggle user active status:", error);
      alert("Failed to update user status. Please try again.");
    }
  };

  const resetForm = () => {
    setFormData({
      phone: "",
      email: "",
      first_name: "",
      last_name: "",
      is_admin: false,
      is_super_admin: false,
      is_active: true,
    });
  };

  const filteredUsers = users.filter((user) => {
    const searchLower = searchTerm.toLowerCase();
    return (
      user.email?.toLowerCase().includes(searchLower) ||
      user.phone?.toLowerCase().includes(searchLower) ||
      user.first_name?.toLowerCase().includes(searchLower) ||
      user.last_name?.toLowerCase().includes(searchLower)
    );
  });

  const getRoleBadge = (user: UserRead) => {
    if (user.is_super_admin) {
      return (
        <Badge variant="default" className="bg-purple-600">
          Super Admin
        </Badge>
      );
    }
    if (user.is_admin) {
      return (
        <Badge variant="default" className="bg-blue-600">
          Admin
        </Badge>
      );
    }
    return <Badge variant="secondary">Customer</Badge>;
  };

  const getInitials = (user: UserRead) => {
    const first = user.first_name?.charAt(0) || "";
    const last = user.last_name?.charAt(0) || "";
    return (
      (first + last).toUpperCase() || user.email?.charAt(0).toUpperCase() || "U"
    );
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">
          User Management
        </h1>
        <div className="flex items-center space-x-3">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <Input
              placeholder="Search users..."
              className="pl-9 w-64"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <Dialog
            open={isCreateDialogOpen}
            onOpenChange={setIsCreateDialogOpen}
          >
            <DialogTrigger asChild>
              <Button
                className="bg-blue-600 hover:bg-blue-700"
                size="sm"
                onClick={() => resetForm()}
              >
                <Plus className="w-4 h-4 mr-2" />
                Create User
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-md">
              <DialogHeader>
                <DialogTitle>Create New User</DialogTitle>
                <DialogDescription>
                  Create a new user account. You can set their role and
                  permissions.
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-4 py-4">
                <div className="space-y-2">
                  <Label htmlFor="phone">Phone *</Label>
                  <Input
                    id="phone"
                    value={formData.phone}
                    onChange={(e) =>
                      setFormData({ ...formData, phone: e.target.value })
                    }
                    placeholder="+1234567890"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email || ""}
                    onChange={(e) =>
                      setFormData({ ...formData, email: e.target.value })
                    }
                    placeholder="user@example.com"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="first_name">First Name</Label>
                    <Input
                      id="first_name"
                      value={formData.first_name || ""}
                      onChange={(e) =>
                        setFormData({ ...formData, first_name: e.target.value })
                      }
                      placeholder="John"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="last_name">Last Name</Label>
                    <Input
                      id="last_name"
                      value={formData.last_name || ""}
                      onChange={(e) =>
                        setFormData({ ...formData, last_name: e.target.value })
                      }
                      placeholder="Doe"
                    />
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="is_admin"
                      checked={formData.is_admin}
                      onCheckedChange={(checked) =>
                        setFormData({
                          ...formData,
                          is_admin: checked as boolean,
                        })
                      }
                    />
                    <Label htmlFor="is_admin" className="cursor-pointer">
                      Admin
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="is_super_admin"
                      checked={formData.is_super_admin}
                      onCheckedChange={(checked) =>
                        setFormData({
                          ...formData,
                          is_super_admin: checked as boolean,
                        })
                      }
                    />
                    <Label htmlFor="is_super_admin" className="cursor-pointer">
                      Super Admin
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="is_active"
                      checked={formData.is_active}
                      onCheckedChange={(checked) =>
                        setFormData({
                          ...formData,
                          is_active: checked as boolean,
                        })
                      }
                    />
                    <Label htmlFor="is_active" className="cursor-pointer">
                      Active
                    </Label>
                  </div>
                </div>
              </div>
              <DialogFooter>
                <Button
                  variant="outline"
                  onClick={() => setIsCreateDialogOpen(false)}
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleCreate}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  Create User
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Users Table */}
      <Card>
        <CardHeader>
          <CardTitle>All Users ({filteredUsers.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-8 text-gray-500">
              Loading users...
            </div>
          ) : filteredUsers.length === 0 ? (
            <div className="text-center py-8 text-gray-500">No users found</div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>User</TableHead>
                  <TableHead>Contact</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredUsers.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell>
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-medium text-sm">
                          {getInitials(user)}
                        </div>
                        <div>
                          <div className="font-medium">
                            {user.first_name || user.last_name
                              ? `${user.first_name || ""} ${
                                  user.last_name || ""
                                }`.trim()
                              : "No Name"}
                          </div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="space-y-1">
                        {user.email && (
                          <div className="text-sm text-gray-600">
                            {user.email}
                          </div>
                        )}
                        {user.phone && (
                          <div className="text-sm text-gray-500">
                            {user.phone}
                          </div>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>{getRoleBadge(user)}</TableCell>
                    <TableCell>
                      <Badge
                        variant={user.is_active ? "default" : "secondary"}
                        className={
                          user.is_active ? "bg-green-600" : "bg-gray-400"
                        }
                      >
                        {user.is_active ? "Active" : "Inactive"}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm text-gray-500">
                      {new Date(user.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex items-center justify-end space-x-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleToggleActive(user)}
                          title={user.is_active ? "Deactivate" : "Activate"}
                        >
                          {user.is_active ? (
                            <UserX className="w-4 h-4 text-gray-600" />
                          ) : (
                            <UserCheck className="w-4 h-4 text-green-600" />
                          )}
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEdit(user)}
                          title="Edit"
                        >
                          <Edit className="w-4 h-4 text-blue-600" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => {
                            setSelectedUser(user);
                            setIsDeleteDialogOpen(true);
                          }}
                          title="Delete"
                        >
                          <Trash2 className="w-4 h-4 text-red-600" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* Edit Dialog */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Edit User</DialogTitle>
            <DialogDescription>
              Update user information and permissions.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="edit-phone">Phone *</Label>
              <Input
                id="edit-phone"
                value={formData.phone}
                onChange={(e) =>
                  setFormData({ ...formData, phone: e.target.value })
                }
                placeholder="+1234567890"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-email">Email</Label>
              <Input
                id="edit-email"
                type="email"
                value={formData.email || ""}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
                placeholder="user@example.com"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="edit-first_name">First Name</Label>
                <Input
                  id="edit-first_name"
                  value={formData.first_name || ""}
                  onChange={(e) =>
                    setFormData({ ...formData, first_name: e.target.value })
                  }
                  placeholder="John"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-last_name">Last Name</Label>
                <Input
                  id="edit-last_name"
                  value={formData.last_name || ""}
                  onChange={(e) =>
                    setFormData({ ...formData, last_name: e.target.value })
                  }
                  placeholder="Doe"
                />
              </div>
            </div>
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="edit-is_admin"
                  checked={formData.is_admin}
                  onCheckedChange={(checked) =>
                    setFormData({ ...formData, is_admin: checked as boolean })
                  }
                />
                <Label htmlFor="edit-is_admin" className="cursor-pointer">
                  Admin
                </Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="edit-is_super_admin"
                  checked={formData.is_super_admin}
                  onCheckedChange={(checked) =>
                    setFormData({
                      ...formData,
                      is_super_admin: checked as boolean,
                    })
                  }
                />
                <Label htmlFor="edit-is_super_admin" className="cursor-pointer">
                  Super Admin
                </Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="edit-is_active"
                  checked={formData.is_active}
                  onCheckedChange={(checked) =>
                    setFormData({ ...formData, is_active: checked as boolean })
                  }
                />
                <Label htmlFor="edit-is_active" className="cursor-pointer">
                  Active
                </Label>
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setIsEditDialogOpen(false)}
            >
              Cancel
            </Button>
            <Button
              onClick={handleUpdate}
              className="bg-blue-600 hover:bg-blue-700"
            >
              Update User
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Dialog */}
      <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete User</DialogTitle>
            <DialogDescription>
              Are you sure you want to deactivate this user? This action will
              set the user as inactive.
              {selectedUser && (
                <div className="mt-2 font-medium">
                  {selectedUser.first_name || selectedUser.last_name
                    ? `${selectedUser.first_name || ""} ${
                        selectedUser.last_name || ""
                      }`.trim()
                    : selectedUser.email || selectedUser.phone}
                </div>
              )}
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setIsDeleteDialogOpen(false)}
            >
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDelete}>
              Deactivate User
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
