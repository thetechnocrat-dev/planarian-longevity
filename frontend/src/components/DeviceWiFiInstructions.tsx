import React, { useEffect, useState } from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Typography, Box } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useParams } from 'react-router-dom';
import api from '../api/axiosConfig';
import { Device } from '../types';

const DeviceWiFiInstructions: React.FC = () => {
  const { register_id } = useParams<{ register_id: string }>();
  const [device, setDevice] = useState<Device | null>(null);

  useEffect(() => {
    if (register_id) {
      fetchDeviceDetails(register_id)
        .then(response => setDevice(response.data))
        .catch(error => console.error('Error fetching device details:', error));
    }
  }, [register_id]);

  const fetchDeviceDetails = async (registerId: string) => {
    return await api.get(`/devices/${registerId}`);
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 600, margin: '0 auto', mt: 4 }}>
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Tufts University WiFi Setup</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            {device ? (
              <>
                1. Go to the <a href="https://device-registration.it.tufts.edu">Tufts Network Registration Form</a> and provide the following MAC Address: {device.mac_address}.
                <br />
                <br />
                2. Wait at least 5 minutes for the device to become registered in the system.
                <br />
                <br />
                3. Power on the device, and it should automatically connect. If you see `openzyme_local` appear as a WiFi network option, it means the device did not connect to Tufts Wireless and reverted back to its local network. If this happens, turn off the device and try again in 5 minutes. If problems persist, please email <a href="mailto:it@tufts.edu">it@tufts.edu</a> and CC <a href="mailto:josh.mcmenemy@openzyme.bio">josh.mcmenemy@openzyme.bio</a>. Include the device's MAC address in the email message.
                <br />
                <br />
                4. If you don't see the `openzyme_local` network appear after powering on the device, then navigate to your <a href={`/devices/${device.register_id}`}>device detail page</a> to view data from your device.
              </>
            ) : (
              <Typography color="error">Device details could not be loaded.</Typography>
            )}
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Home/Office WiFi Setup</Typography>
        </AccordionSummary>
        <AccordionDetails>
        <Typography>
          {device ? (
            <>
              1. Power on the device and wait for `openzyme_local` to appear as a network option in your WiFi connection options. If `openzyme_local` does not appear, restart the device. If the problem persists, please email <a href="mailto:josh.mcmenemy@openzyme.bio">josh.mcmenemy@openzyme.bio</a>.
              <br />
              <br />
              2. Connect your computer to `openzyme_local` (you will lose internet access while connected to `openzyme_local`).
              <br />
              <br />
              3. Navigate to `http://192.168.50.1:8080/` and fill out the form with your WiFi name and password.
              <br />
              <br />
              4. If the webpage freezes upon submission, it means the device has already switched over to the provided network. You can go ahead and switch back your network and navigate to your <a href={`/devices/${device.register_id}`}>device detail page</a> to view data from your device.
              <br />
              <br />
              5. If the form submits, but the `openzyme_local` network remains active, restart the device and retry submitting the form.
              <br />
              <br />
              6. If the problem persists, please email <a href="mailto:josh.mcmenemy@openzyme.bio">josh.mcmenemy@openzyme.bio</a>.
            </>
          ) : (
            <Typography color="error">Device details could not be loaded.</Typography>
          )}
        </Typography>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

export default DeviceWiFiInstructions;
