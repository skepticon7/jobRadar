# JobRadar – Installation Guide

This guide explains how to set up and run the JobRadar backend project locally after cloning the repository.

---

## 🧰 2/6 – Requirements

- Python 3.8 or higher
- Git
- `virtualenv` (recommended)

---

## 🔧 3/6 – Installation Steps

### Step 1: Clone the repository

```bash
git clone https://github.com/skepticon7/jobRadar.git
cd JobRadar
```

### Step 2 : Create a virtual environment

```bash
python -m venv venv
```

### Step 3 : Activate the virtual environment

```bash
venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

#### if the requirements.txt file is missing , generate it !

```bash
pip freeze > requirements.txt
```


### Step 5 : Apply database migrations

```bash
Step 5: Apply database migrations
```
```bash
python manage.py migrate
```



