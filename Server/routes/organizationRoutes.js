import express from 'express';
import { 
  createOrganizations, 
  updateOrganization, 
  updateOrganizationCategory,
  getAllOrganizations,
  getOrganizationById,
  getOrganizationByAbbreviation,
  getOrganizationsByCategory
} from '../controller/organizationController.js';

const router=express.Router();

// GET routes for fetching organizations
router.get('/categories', getAllCategories);
router.get('/authorities', getAllAuthorities);
router.get('/organizations', getAllOrganizations);
router.get('/organizations/id/:id', getOrganizationById);
router.get('/organizations/abbreviation/:abbreviation', getOrganizationByAbbreviation);
router.get('/organizations/category/:categoryName', getOrganizationsByCategory);

// POST routes for creating/updating organizations
router.post('/createOrganizations',createOrganizations);
router.post('/updateOrganization',updateOrganization);
router.post('/updateOrganizationCategory',updateOrganizationCategory);

export default router;