# 🚀 DevOps Project – FastAPI, Terraform, Docker, Ansible, CI/CD

Ce projet met en œuvre une application FastAPI déployée automatiquement sur une instance EC2 d’AWS grâce à Terraform, Docker, GitHub Actions (CI/CD) et Ansible pour l’automatisation de la configuration.

---

## 📁 Structure du projet


---

## 🚧 Fonctionnalités

- 🌐 **API backend** : construite avec [FastAPI](https://fastapi.tiangolo.com/)
- ☁️ **Infrastructure as Code** : provisionnement d’une instance EC2 avec [Terraform](https://www.terraform.io/)
- 🐳 **Conteneurisation** : l'application tourne dans un conteneur Docker
- ⚙️ **Déploiement automatisé** : via [GitHub Actions](https://github.com/features/actions)
- 📦 **Publication d’image Docker** : dans GitHub Container Registry (GHCR)
- 🛠️ **Ansible** (à venir) : configuration automatique de l’instance EC2
- ✅ **Linting & Sécurité** : via `black` et `bandit`
- 🧪 **Tests automatisés** avec `pytest`

---

## 🚀 Lancer en local (dev)

```bash
# Depuis la racine
docker compose -f docker/docker-compose.yml up --build
```
Accessible sur : [http://127.0.0.1:4000](http://127.0.0.1:4000)

---

## 🛠️ Infrastructure AWS avec Terraform
```bash
cd terraform
terraform init
terraform validate
terraform plan
terraform apply
```

---

## ⚙️ CI/CD avec GitHub Actions

Deux pipelines :
- ci.yml : Lint, test et build/push de l’image Docker (main, develop, feature/*)
- terraform.yml : Provisionne EC2 avec Terraform (uniquement sur main)

---

## ✅ Exemple de route de santé

```bash
@app.get("/healthcheck")
def healthcheck():
    return {
        "status": "ok",
        "version": __version__
    }
```

## 📧 Contact

Projet réalisé par Saad R. dans un cadre devops personnel.
N'hésitez pas à ouvrir une issue ou une PR pour discuter des améliorations !
