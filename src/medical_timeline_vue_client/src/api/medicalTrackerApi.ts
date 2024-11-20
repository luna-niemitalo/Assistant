// src/api/medicalTrackerApi.ts
import axiosInstance from './axiosInstance';

export interface EventData {
    title: string;
    user_id: number;
    event_type: string;
    severity?: number;
    timestamp?: number;
    falloff?: string;
    start_time?: string;
    end_time?: string;
    symptom: boolean;
    category: string;
    notes?: string;
    tags?: number;
}

export const addEvent = async (eventData: EventData) => {
    const response = await axiosInstance.post('/events', eventData);
    return response.data;
};

export const getTagsMapping = async () => {
    const response = await axiosInstance.get('/tags/mapping');
    return response.data;
};

export const getTagsFromBinary = async (binary: number) => {
    const response = await axiosInstance.post('/tags/from_binary', { binary });
    return response.data;
};

export const getBinaryFromTags = async (tags: string[]) => {
    const response = await axiosInstance.post('/tags/to_binary', { tags });
    return response.data;
};
