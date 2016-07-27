package org.esa.snap.dataio.nc4;

import org.esa.snap.core.dataio.EncodeQualification;
import org.esa.snap.core.datamodel.*;
import org.esa.snap.core.image.ImageManager;
import org.esa.snap.dataio.netcdf.AbstractNetCdfWriterPlugIn;
import org.esa.snap.dataio.netcdf.ProfileWriteContext;
import org.esa.snap.dataio.netcdf.metadata.ProfileInitPartWriter;
import org.esa.snap.dataio.netcdf.metadata.ProfilePartWriter;
import org.esa.snap.dataio.netcdf.metadata.profiles.beam.*;
import org.esa.snap.dataio.netcdf.metadata.profiles.cf.CfBandPart;
import org.esa.snap.dataio.netcdf.nc.NFileWriteable;
import org.esa.snap.dataio.netcdf.nc.NVariable;
import org.esa.snap.dataio.netcdf.nc.NWritableFactory;
import org.esa.snap.dataio.netcdf.util.DataTypeUtils;
import org.geotools.referencing.CRS;
import org.geotools.referencing.crs.DefaultGeographicCRS;

import java.awt.*;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Locale;
import java.util.TimeZone;

/**
 * Writer plugin for NetCDF4 output adapted to SNAP CAWA requirements
 * (i.e. keep products as small as possible)
 *
 * @author olafd
 */
public class SnapCawaNc4WriterPlugIn extends AbstractNetCdfWriterPlugIn {

    public String[] getFormatNames() {
        return new String[]{"NetCDF4-CAWA"};
    }

    public String[] getDefaultFileExtensions() {
        return new String[]{".nc"};
    }

    public String getDescription(Locale locale) {
        return "SNAP CAWA NetCDF4 products";
    }

    @Override
    public ProfilePartWriter createFlagCodingPartWriter() {
        return new BeamFlagCodingPart();
    }

    @Override
    public ProfilePartWriter createMetadataPartWriter() {
        return new BeamMetadataPart();
    }

    @Override
    public ProfilePartWriter createTiePointGridPartWriter() {
        return new BeamTiePointGridPart();
    }

    @Override
    public ProfilePartWriter createGeoCodingPartWriter() {
        return new SnapCawaGeocodingPart();  // use this instead of BeamGeocodingPart
    }

    @Override
    public ProfilePartWriter createMaskPartWriter() {
        return new BeamMaskPart();
    }

    @Override
    public ProfileInitPartWriter createInitialisationPartWriter() {
        return new SnapCawaMainPart();
    }

    @Override
    public NFileWriteable createWritable(String outputPath) throws IOException {
        return NWritableFactory.create(outputPath, "netcdf4");
    }

    public EncodeQualification getEncodeQualification(Product product) {
        if (product.isMultiSize()) {
            return new EncodeQualification(EncodeQualification.Preservation.UNABLE,
                    "Cannot write multisize products. Consider resampling the product first.");
        }
        return new EncodeQualification(EncodeQualification.Preservation.PARTIAL);
    }

    private class SnapCawaMainPart implements ProfileInitPartWriter {

        private final SimpleDateFormat COMPACT_ISO_FORMAT = new SimpleDateFormat("yyyyMMdd'T'HHmmss'Z'");
        private Dimension tileSize;

        SnapCawaMainPart() {
            COMPACT_ISO_FORMAT.setTimeZone(TimeZone.getTimeZone("UTC"));
        }

        public void writeProductBody(ProfileWriteContext ctx, Product product) throws IOException {
            NFileWriteable writeable = ctx.getNetcdfFileWriteable();
            tileSize = ImageManager.getPreferredTileSize(product);

            if (isGeographicCRS(product.getSceneGeoCoding())) {
                writeDimensions(writeable, product, "lat", "lon");
            } else {
                writeDimensions(writeable, product, "y", "x");
            }

            addGlobalAttributes(writeable, product);

            for (Band b : product.getBands()) {
                final String bandName = b.getName();
                if (bandName.equals("tcwv")) {
                    addNc4VariableAttribute(writeable, b);

                } else if (bandName.endsWith("flags")) {
                    addNc4VariableAttribute(writeable, b);
                }
            }
        }

        private void writeDimensions(NFileWriteable writeable, Product p, String dimY, String dimX) throws IOException {
            writeable.addDimension(dimY, p.getSceneRasterHeight());
            writeable.addDimension(dimX, p.getSceneRasterWidth());
        }

        private boolean isGeographicCRS(final GeoCoding geoCoding) {
            return (geoCoding instanceof CrsGeoCoding) &&
                    CRS.equalsIgnoreMetadata(geoCoding.getMapCRS(), DefaultGeographicCRS.WGS84);
        }

        private void addGlobalAttributes(NFileWriteable writeable, Product product) throws IOException {
            writeable.addGlobalAttribute("Conventions", "CF-1.4");
            writeable.addGlobalAttribute("title", "CAWA TCWV product");
            writeable.addGlobalAttribute("product_type", product.getProductType());

            writeable.addGlobalAttribute("start_date", product.getStartTime().format());
            writeable.addGlobalAttribute("stop_date", product.getEndTime().format());
            writeable.addGlobalAttribute("TileSize", tileSize.height + ":" + tileSize.width);
            // the 'metadata_profile' attribute is required to make SNAP use the BEAM NetCDF reader when
            // reading this product!!
            writeable.addGlobalAttribute("metadata_profile", "beam");
            writeable.addGlobalAttribute("metadata_version", "0.5");
        }

        private void addNc4VariableAttribute(NFileWriteable writeable, RasterDataNode b) throws IOException {
            NVariable variable = writeable.addVariable(b.getName(),
                    DataTypeUtils.getNetcdfDataType(b.getDataType()),
                    tileSize, writeable.getDimensions());

            variable.addAttribute("coordinates", "latitude longitude");
            CfBandPart.writeCfBandAttributes(b, variable);
            BeamBandPart.writeBeamBandAttributes((Band) b, variable);
        }
    }
}
