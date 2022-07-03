const { res } = require("express");

const Pool = require('pg').Pool;

const pool = new Pool({
  user: 'byron',
  host: 'localhost',
  database: 'buses',
  password: 'Field2703',
  port: 5432
});

const getAllStops = async (req, res) => {
    pool.query('SELECT * FROM stop;', (error, results) => {
        res.status(200).json(results.rows);
    });
};

const getStopById = async (req, res) => {
    pool.query('SELECT * FROM stop WHERE id = $1;', [1], (error, results) => {
        res.status(200).json(results.rows);
    });
};

const addStop = async (req, res) => {
    const { id, desc } = req.body;
    inMemoryStopes.push({ id, desc });
    res.status(201).send(`Stop added successfully.`);
  };
  
  const updateStop = (req, res) => {
    const { id, desc } = req.body;
    inMemoryStopes[0] = { id, desc };
    res.status(200).send(`First stop in list is updated.`);
  };
  
  const deleteStop = (req, res) => {
    inMemoryStopes.shift();
    res.status(200).send(`First stop in list is deleted.`);
  };

  module.exports = {
    getAllStops,
    getStopById,
    addStop,
    updateStop,
    deleteStop
  };