from typing import List, Dict

import datahub.emitter.mce_builder as builder
import datahub.metadata.schema_classes as models

from dh_client.entities import Entity
from dh_client.entities.tags import Tag
from dh_client.entities.owners import Owner


class Dataset(Entity):
    """
    Examples:

        >>> client.dataset.upsert(name="projectA.datasetB.tableC", description="A random dataset description",
        ...                       tags=["foo"], owners=["team1@domain.com", "user2@domain.com"],
        ...                       glossary_terms=["gloss_term1"], upstream_datasets=["projectA.datasetB.tableD"],
        ...                       links={"Kaggle": "https://kaggle.com/randomuser/randomdataset"},
        ...                       custom_properties={'a': 'b'}
        ... )
    """

    entity_type: str = "dataset"
    aspect_name: str = "datasetProperties"

    def _create_mpc(
        self,
        name: str,
        platform: str = "bigquery",
        env: str = "DEV",
        description: str = None,
        url: str = None,
        tags: List[str] = None,
        owners: List[str] = None,
        custom_properties=None,
        glossary_terms: List[str] = None,
        upstream_datasets: List[str] = None,
        links: dict = None,
    ) -> List[dict]:
        dataset_urn: str = builder.make_dataset_urn(
            platform=platform, name=name, env=env
        )

        mpc = [
            dict(
                entityType=Dataset.entity_type,
                entityUrn=dataset_urn,
                aspectName=Dataset.aspect_name,
                aspect=models.DatasetPropertiesClass(
                    description=description, externalUrl=url
                ),
            )
        ]

        mpc.extend(self._add_tags(tags, dataset_urn))
        mpc.extend(self._add_owners(owners, dataset_urn))
        mpc.extend(self._add_custom_properties(custom_properties, dataset_urn))
        mpc.extend(self._add_glossary_terms(glossary_terms, dataset_urn))
        mpc.extend(self._add_upstream_datasets(dataset_urn, upstream_datasets))
        mpc.extend(self._add_links(dataset_urn, links))

        return mpc

    @staticmethod
    def _add_tags(tags, dataset_urn) -> List[dict]:
        return (
            [
                dict(
                    entityType=Dataset.entity_type,
                    entityUrn=dataset_urn,
                    aspectName="globalTags",
                    aspect=Tag.create_global_tags_aspect(tags),
                )
            ]
            if tags
            else []
        )

    @staticmethod
    def _add_owners(owners, dataset_urn) -> List[dict]:
        return (
            [
                dict(
                    entityUrn=dataset_urn,
                    entityType=Dataset.entity_type,
                    aspectName="ownership",
                    aspect=Owner.create_owners_aspect(owners),
                )
            ]
            if owners
            else []
        )

    @staticmethod
    def _add_custom_properties(custom_properties: dict, dataset_urn: str) -> List[dict]:
        return (
            [
                dict(
                    entityUrn=dataset_urn,
                    entityType=Dataset.entity_type,
                    aspectName="datasetProperties",
                    aspect=models.DatasetPropertiesClass(
                        customProperties=custom_properties
                    ),
                )
            ]
            if custom_properties
            else []
        )

    def _add_glossary_terms(
        self, glossary_terms: List[str], dataset_urn: str
    ) -> List[dict]:
        return (
            [
                dict(
                    entityUrn=dataset_urn,
                    aspectName="glossaryTerms",
                    entityType=Dataset.entity_type,
                    aspect=models.GlossaryTermsClass(
                        terms=[
                            models.GlossaryTermAssociationClass(
                                f"urn:li:glossaryTerm:{term}"
                            )
                            for term in glossary_terms
                        ],
                        auditStamp=models.AuditStampClass(
                            time=0, actor=self.emmiter.datahub_actor
                        ),
                    ),
                )
            ]
            if glossary_terms
            else []
        )

    def _add_upstream_datasets(
        self, dataset_urn: str, upstream_datasets: List[str]
    ) -> List[dict]:
        return (
            [
                {
                    "entityUrn": dataset_urn,
                    "aspectName": "upstreamLineage",
                    "entityType": Dataset.entity_type,
                    "aspect": models.UpstreamLineageClass(
                        upstreams=[
                            models.UpstreamClass(
                                dataset=builder.make_dataset_urn(
                                    platform=self.emmiter.dataset_platform,
                                    name=upstream_dataset,
                                    env=self.emmiter.env,
                                ),
                                type=models.DatasetLineageTypeClass.TRANSFORMED,
                            )
                            for upstream_dataset in upstream_datasets
                        ]
                    ),
                }
            ]
            if upstream_datasets
            else []
        )

    def _add_links(self, dataset_urn: str, links: Dict[str, str]) -> List[dict]:
        return (
            [
                {
                    "entityUrn": dataset_urn,
                    "entityType": Dataset.entity_type,
                    "aspectName": "institutionalMemory",
                    "aspect": models.InstitutionalMemoryClass(
                        elements=[
                            models.InstitutionalMemoryMetadataClass(
                                url=links[desc],
                                description=desc,
                                createStamp=models.AuditStampClass(
                                    time=0, actor=self.emmiter.datahub_actor
                                ),
                            )
                            for desc in links.keys()
                        ]
                    ),
                }
            ]
            if links
            else []
        )

    def delete_tag(self, dataset_urn: str, tag: str) -> None:
        """Delete tag from a dataset

        Examples:

            >>> client.dataset.delete_tag("projectA.datasetB.tableC", "foo")
        """
        body = {
            "query": "mutation removeTag($input: TagAssociationInput!) {removeTag(input: $input)}",
            "variables": {
                "input": {
                    "tagUrn": builder.make_tag_urn(tag),
                    "resourceUrn": self._create_resource_urn(dataset_urn),
                }
            },
        }
        self._apply_mcp(None, [body], use_graphql=True)

    def _create_resource_urn(self, dataset_urn: str) -> str:
        return builder.make_dataset_urn(
            self.emmiter.dataset_platform, dataset_urn, self.emmiter.env
        )
