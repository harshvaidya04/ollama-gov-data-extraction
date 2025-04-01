import express from "express";
import { addEvent, createEventType, deleteEvent } from "../controller/eventController.js";

const router = express.Router();

router.post('/createEventType',createEventType);
router.post('/addEvent',addEvent);
router.post('/delete', deleteEvent);

export default router;