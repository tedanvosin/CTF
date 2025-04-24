const cameraStatus = [
    {
        id: 1,
        name: 'Main Entrance',
        location: 'Building A - Front Door',
        status: 'active',
        url: 'img/front_door-building_a.png'
    },
    {
        id: 2,
        name: 'Parking Lot',
        location: 'Building A - Parking Area',
        status: 'active',
        url: 'img/parking_lot-building_a.png'
    },
    {
        id: 3,
        name: 'Back Entrance',
        location: 'Building A - Back Door',
        status: 'active',
        url: 'img/back_door-building_a.png'
    },
    {
        id: 4,
        name: 'Server Room',
        location: 'Building B - Server Room',
        status: 'active',
        url: 'img/server_room-building_b.png'
    },
    { 
        id: 5, 
        name: 'Emergency Exit', 
        location: 'East Wing', 
        status: 'active',
        url: 'img/emergency_exit-east_wing.png'
    },
    { 
        id: 6, 
        name: 'Reception Area', 
        location: 'Main Building', 
        status: 'active',
        url: 'img/reception_area-main_building.png'
    }
];

const getAllCameras = (req, res) => {
    res.json(cameraStatus);
};

const enableCamera = (req, res) => {
    const { id } = req.params;
    const camera = cameraStatus.find(c => c.id === parseInt(id));
    
    if (camera) {
        camera.status = 'active';
        res.json({ success: true, message: `Camera ${id} enabled` });
    } else {
        res.status(404).json({ success: false, message: 'Camera not found' });
    }
};

const disableCamera = (req, res) => {
    const { id } = req.params;
    const camera = cameraStatus.find(c => c.id === parseInt(id));
    
    if (camera) {
        camera.status = 'disabled';
        res.json({ success: true, message: `Camera ${id} disabled` });
    } else {
        res.status(404).json({ success: false, message: 'Camera not found' });
    }
};

const getFlag = (req, res) => {
    // Check if all cameras are disabled
    const allDisabled = cameraStatus.every(camera => camera.status === 'disabled');
    if (allDisabled) {
        res.json({ 
            success: true, 
            flag: process.env.FLAG
        });
    } else {
        res.status(403).json({ 
            success: false, 
            message: 'All cameras must be disabled to get the flag' 
        });
    }
};

module.exports = {
    getAllCameras,
    enableCamera,
    disableCamera,
    getFlag
}; 