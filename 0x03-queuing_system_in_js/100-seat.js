#!/usr/bin/yarn dev
import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';

const app = express();
const client = createClient({ name: 'reserve_seat' });
const queue = createQueue();
const ORIGINAL_SEATS_COUNT = 50;
const reservationEnabled = false;
const PORT = 1245;
const getAsync = promisify(client.GET).bind(client);
const setAsync = promisify(client.SET).bind(client);

/**
 * Modifies the number of available seats.
 * @param {number} number - The new number of seats.
 */
const reserveSeat = async (number) => {
    return setAsync('available_seats', number);
};

/**
 * Retrieves the number of available seats.
 * @returns {Promise<String>}
 */
const getCurrentAvailableSeats = async () => {
    return getAsync('available_seats');
};

app.get('/available_seats', async (req, res) => {
    const availableSeats = await getCurrentAvailableSeats();
    res.json(availableSeats);
});

app.get('/reserve_seat', async (req, res) => {
    if (!reservationEnabled) {
        res.json({ status: 'Reservation are blocked' });
        return;
    }
    try {
        const job = queue.create('reserve_seat');

        job.on('failed', (err) => {
            console.log(
                'Seat reservation job',
                job.id,
                'failed:',
                err.message || err.toString(),
            );
        });
        job.on('complete', () => {
            console.log(
                'Seat reservation job',
                job.id,
                'completed'
            );
        });
        job.save();
        res.json({ status: 'Reservation in process' });
    } catch {
        res.json({ status: 'Reservation failed' });
    }
});

app.get('/process', (req, res) => {
    res.json({ status: 'Queue processing' });
    queue.process('reserve_seat', async(job, done) => {
        getCurrentAvailableSeats()
            .then((result) => Number.parseInt(result || 0))
            .then((availableSeats) => {
                reservationEnabled = availableSeats <= 1 ? false : reservationEnabled;
                if (availableSeats >= 1) {
                    reserveSeat(availableSeats - 1)
                        .then(() => done());
                } else {
                    done(new Error('Not enough seats available'));
                }
            });
    });
});

const resetAvailableSeats = async (initialSeatsCount) => {
    return setAsync('available_seats', Number.parseInt(initialSeatsCount));
};

app.listen(PORT, () => {
    resetAvailableSeats(process.env.ORIGINAL_SEATS_COUNT || ORIGINAL_SEATS_COUNT)
        .then(() => {
            reservationEnabled = true;
            console.log(`API available on localhost port ${PORT}`);
        });
});

export default app;