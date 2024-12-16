FROM rockylinux:9

RUN dnf update -y && \
    dnf -y --allowerasing install \
        procps-ng tmux git curl wget rsync vim diffutils iproute iputils nmap-ncat && \
    dnf install -y openssh-clients && \
    dnf install -y openssh-server && \
    ssh-keygen -A && \
    dnf install -y epel-release && \
    dnf install -y zip unzip && \
    dnf install -y tesseract python3-img2pdf poppler-utils && \
    dnf install -y make perl pdftk && \
    useradd -s /bin/bash -m om && \
    (echo "om:welcome" | chpasswd) && \
    dnf -y install sudo && \
    (echo 'om ALL=(ALL) NOPASSWD: ALL' >/etc/sudoers.d/om) && \
    echo

#EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
