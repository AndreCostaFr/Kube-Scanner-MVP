from kubernetes import client, config

def get_k8s_images():
    print("🔌 Connecting to K8s cluster...")
    
    config.load_kube_config()
    
    v1 = client.CoreV1Api()
    
    print("🔎 Fetching pods from all namespaces...")
    
    pods = v1.list_pod_for_all_namespaces(watch=False)
    
    images_list = []
    
    for pod in pods.items:
        if pod.status.phase != "Running":
            continue
            
        namespace = pod.metadata.namespace
        pod_name = pod.metadata.name

        for container in pod.spec.containers:
            image_name = container.image
            images_list.append({
                "pod": pod_name,
                "namespace": namespace,
                "image": image_name
            })
            
            print(f"   📌 Pod: {pod_name} ({namespace}) -> Image: {image_name}")

    return images_list

if __name__ == "__main__":
    images = get_k8s_images()
    print(f"\n✅ Success! Found {len(images)} running containers.")